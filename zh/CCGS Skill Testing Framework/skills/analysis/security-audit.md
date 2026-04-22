# 技能测试规范：/security-audit

## 技能概要

`/security-audit` 审计 `src/` 中的游戏代码，检查安全漏洞，包括：
存档数据完整性（是否加密/签名）、网络认证（在线功能是否有身份验证）、
反作弊措施、数据隐私合规（是否未暴露凭据）和输入验证（是否检查网络输入）。

技能为只读——仅生成调查结果，不应用修复。不写入报告文件——
发现内容以结构化形式直接输出。
无 director 门控（但建议咨询 security-engineer agent）。
判定结果：SECURE（未发现漏洞）、CONCERNS（存在潜在风险但非严重）
或 VULNERABILITIES FOUND（存在必须在发布前修复的严重问题）。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：SECURE、CONCERNS、VULNERABILITIES FOUND
- [ ] 不包含"May I write"语言（security-audit 为只读技能）
- [ ] 包含下一步交接（例如 `/hotfix` 修复严重漏洞，或建议咨询 security-engineer）

---

## Director 门控检查

无。`/security-audit` 是只读分析技能，不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——存档已加密，无凭据暴露，SECURE

**夹具：**
- `src/core/SaveManager.gd`：存档数据在写入磁盘前加密
- `src/`：grep 未发现 API_KEY、PASSWORD、SECRET 等硬编码字符串
- `src/networking/`：所有网络请求均有身份验证令牌

**输入：** `/security-audit`

**预期行为：**
1. 技能扫描 `src/` 进行安全检查
2. 检查项 1：存档数据加密——通过
3. 检查项 2：无硬编码凭据——通过
4. 检查项 3：网络认证——通过
5. 0 个漏洞
6. 判定结果为 SECURE

**断言：**
- [ ] 检查存档数据加密
- [ ] grep 硬编码凭据（API_KEY、PASSWORD、SECRET）
- [ ] 检查网络认证是否存在
- [ ] 0 个漏洞 → 判定结果为 SECURE
- [ ] 不修改任何文件

---

### 用例 2：未加密存档 + 暴露版本字符串——VULNERABILITIES FOUND

**夹具：**
- `src/core/SaveManager.gd`：以明文 JSON 写入存档（无加密）
- `src/networking/ApiClient.gd`：HTTP 响应头包含 `Server-Version: Godot4.2`
  （暴露版本信息）

**输入：** `/security-audit`

**预期行为：**
1. 技能检测到存档以明文 JSON 写入——HIGH 严重性（存档篡改漏洞）
2. 技能检测到版本字符串暴露——MEDIUM 严重性（信息泄露）
3. 报告列出两个漏洞，附严重性和修复指导
4. 判定结果为 VULNERABILITIES FOUND

**断言：**
- [ ] 检测到未加密存档（HIGH 严重性）
- [ ] 检测到版本字符串暴露（MEDIUM 严重性）
- [ ] 报告提供每个漏洞的修复指导
- [ ] 判定结果为 VULNERABILITIES FOUND（非 CONCERNS）
- [ ] 不修改任何文件

---

### 用例 3：无认证的在线功能——CONCERNS

**夹具：**
- `src/networking/` 存在（游戏有在线功能）
- HTTP 请求无认证头（无 Bearer 令牌，无会话验证）

**输入：** `/security-audit`

**预期行为：**
1. 技能检测到在线功能（存在网络代码）
2. 技能检查认证——无认证机制
3. 技能将此标记为 CONCERNS（MEDIUM 严重性）：
   "Online feature detected but no authentication mechanism found.
   Recommend adding player authentication before public release."
4. 判定结果为 CONCERNS

**断言：**
- [ ] 检测到在线功能
- [ ] 识别缺少认证机制
- [ ] 标记为 MEDIUM 严重性 CONCERNS
- [ ] 判定结果为 CONCERNS（非 VULNERABILITIES FOUND——尚未明确利用，但有风险）

---

### 用例 4：无 src/ 文件——报告错误

**夹具：**
- `src/` 目录不存在或为空

**输入：** `/security-audit`

**预期行为：**
1. 技能尝试扫描 `src/`——目录不存在或无文件
2. 技能输出："No source files found in `src/`. Cannot perform security audit."
3. 不生成判定
4. 技能礼貌退出

**断言：**
- [ ] 检测到无源文件
- [ ] 输出清晰的错误信息
- [ ] 不生成部分/无效的安全报告
- [ ] 不写入任何文件

---

### 用例 5：门控合规性——无 director 门控；建议 security-engineer

**夹具：**
- `src/` 包含可分析的源文件

**输入：** `/security-audit`

**预期行为：**
1. 技能完成安全审计
2. 未调用 director 门控
3. 若发现严重漏洞，报告建议咨询 security-engineer agent

**断言：**
- [ ] 未调用任何 director 门控
- [ ] 发现严重漏洞时建议咨询 security-engineer（可选，非强制）
- [ ] 不写入任何文件

---

## 协议合规性

- [ ] 检查存档加密、凭据暴露、网络认证和输入验证
- [ ] 按严重性（HIGH/MEDIUM/LOW）对漏洞进行分类
- [ ] 报告提供每个漏洞的修复指导
- [ ] 不修改任何源文件（完全只读）
- [ ] 返回 SECURE、CONCERNS 或 VULNERABILITIES FOUND 判定

---

## 覆盖说明

- 特定平台的安全问题（iOS App Transport Security、Android 网络安全配置）
  遵循相同的检查模式，但需要特定平台知识；此处未单独测试。
- OWASP Top 10 游戏安全检查由此技能的检查覆盖，但此处不对
  OWASP 特定编号（例如 OWASP-G1）进行断言测试。
- 对实时多人游戏（权威服务器 vs. 客户端作弊检测）的审计
  此处未测试，超出基础安全扫描范围，由专项反作弊审计处理。
