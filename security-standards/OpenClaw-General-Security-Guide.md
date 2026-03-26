# 🛡️ OpenClaw 系統安全與合規操作指南 (通用版)

## 前言：AI Agent 的主權與責任
OpenClaw 是一個高度可擴展的 AI Agent 框架。由於其具備多種 MCP 工具連結（如 Filesystem, Google Workspace, Terminal 等），確保系統的「主權」在人類手中是運行的首要前提。

---

## 一、 架構安全與隔離 (Architecture & Isolation)

1.  **沙盒化執行 (Sandboxing)**：
    *   Agent 的主運行環境必須在沙盒容器（如 Docker）中。
    *   禁止賦予沙盒過高的 Host 權限（如 `--privileged`），除非該任務確實需要操作系統內核。
2.  **工作區分離 (Workspace Separation)**：
    *   Agent 只能讀寫 `/home/node/.openclaw/workspace` 下的內容。
    *   對於系統關鍵配置（如 `/etc`, `/root`），應設定為唯讀或完全隔離。
3.  **權限最小化 (Least Privilege)**：
    *   若任務僅需讀取檔案，請使用唯讀掛載。
    *   不同的 Subagent 應根據職責（如市場分析 vs. 代碼撰寫）分配不同的模型與權限。

---

## 二、 指令執行與審核機制 (Exec & Approval)

1.  **啟用審批流程**：
    *   所有具備破壞性或敏感操作的指令，必須通過 `/approve` 機制。
    *   **嚴禁使用 `allow-always`** 給予 `rm`, `mkfs`, `git push --force` 等高風險命令，建議每次手動審核。
2.  **腳本審查 (Script Review)**：
    *   在執行 Agent 產生的複雜腳本前，要求 Agent 必須先解釋腳本邏輯。
    *   避免直接執行下載自網路的二進位檔案或不明腳本。
3.  **日誌監控 (Logging)**：
    *   定期使用 `openclaw status` 與 `logs` 檢查異常活動。
    *   注意 Session 的運行時長，若單一任務執行超過 30 分鐘，可能存在死循環或資源浪費。

---

## 三、 憑證管理與資料隱私 (Secrets & Privacy)

1.  **禁止靜態存儲 API Key**：
    *   **絕對不要**將 API Keys 或密碼直接寫在 `AGENTS.md`, `TOOLS.md` 或 `MEMORY.md` 中。
    *   應使用 `openclaw secrets set` 將憑證存入系統加密存儲，或透過 `.env` 檔案在啟動時注入。
2.  **PII (個人識別資訊) 保護**：
    *   在將資料傳送給雲端模型（如 OpenAI, Claude, Gemini）前，應檢查是否包含客戶個資或敏感金融數據。
    *   優先在本地使用小型模型（SLM）處理敏感文本清洗任務。
3.  **Gateway 安全**：
    *   確保 `OPENCLAW_GATEWAY_TOKEN` 定期更換。
    *   若需遠端連線，請使用 Tailscale 等 VPN 技術，避免將 Gateway Port 直接曝露在公網。

---

## 四、 子代理與工作流管理 (Orchestration)

1.  **設定超時閾值**：
    *   使用 `sessions_spawn` 時，務必設定 `runTimeoutSeconds`。
    *   對於長時間運行的任務，建議採用「非同步 + 回報」模式，而非主進程死等。
2.  **成本與 Token 熔斷**：
    *   監控各個 Session 的 Token 消耗。
    *   若單次任務預計消耗超過 1,000 萬 Token，應手動暫停並評估必要性。

---

## 五、 應急預案與日常維護

*   **異常行為定義**：頻繁嘗試修改系統路徑、大量重複搜尋、嘗試對外掃描網絡等。
*   **斷路器 (Circuit Breaker)**：若偵測到異常，立即執行 `openclaw gateway stop`。
*   **定期稽核**：每週檢查一次 `skills/` 與 `config/` 是否有未經授權的變動。

---
*版本：v1.0 (2026-03-21) | 適用於所有 OpenClaw 部署環境*
