# Godot 网络 — 快速参考

Last verified: 2026-02-12 | Engine: Godot 4.6

## 自 ~4.3（LLM 截止版本）以来的变更

### 4.6 变更
- **破坏性变更中的网络章节**：4.5→4.6 的具体内容请参阅官方迁移指南

### 4.5 变更
- **无重大网络 API 破坏性变更** — 核心多人 API 保持稳定

## 当前 API 模式

### 高层多人 API
```gdscript
# 服务器端
func host_game(port: int = 9999) -> void:
    var peer := ENetMultiplayerPeer.new()
    peer.create_server(port)
    multiplayer.multiplayer_peer = peer
    multiplayer.peer_connected.connect(_on_peer_connected)
    multiplayer.peer_disconnected.connect(_on_peer_disconnected)

# 客户端
func join_game(address: String, port: int = 9999) -> void:
    var peer := ENetMultiplayerPeer.new()
    peer.create_client(address, port)
    multiplayer.multiplayer_peer = peer
```

### RPC
```gdscript
# 服务器权威模式
@rpc("any_peer", "call_local", "reliable")
func request_action(action_data: Dictionary) -> void:
    if not multiplayer.is_server():
        return
    # 在服务器验证，然后广播
    _execute_action.rpc(action_data)

@rpc("authority", "call_local", "reliable")
func _execute_action(action_data: Dictionary) -> void:
    # 所有对等端执行已验证的动作
    pass
```

### MultiplayerSpawner 与 MultiplayerSynchronizer
```gdscript
# 使用 MultiplayerSpawner 实现节点的自动复制
# 使用 MultiplayerSynchronizer 实现属性同步

# MultiplayerSynchronizer 配置：
# 1. 添加为需要同步的节点的子节点
# 2. 在编辑器中配置复制属性
# 3. 设置可见性过滤器以控制相关性
```

### SceneMultiplayer 配置
```gdscript
func _ready() -> void:
    var scene_mp := multiplayer as SceneMultiplayer
    scene_mp.auth_callback = _authenticate_peer
    scene_mp.server_relay = false  # 直接对等连接

func _authenticate_peer(id: int, data: PackedByteArray) -> void:
    # 自定义认证逻辑
    pass
```

## 常见错误
- 客户端到服务器的 RPC 未使用 `"any_peer"`（默认仅 authority 可调用）
- 未在服务器端验证就信任客户端数据
- 对游戏状态变更使用 `"unreliable"`（仅用于位置更新）
- 生成节点时未设置多人权威（`set_multiplayer_authority()`）
