# Real Case Quality Gate Input

## Project name
AI Assistant Web

## Release name
v1.2.0

## Change scope
- 新增会话置顶功能
- 优化消息重试逻辑
- 调整登录态失效后的跳转流程
- 重构通知发送模块部分代码

## Open high-risk issues
- 通知发送成功率监控未完成最终验证
- 登录态失效场景仅完成主链路回归，边界场景覆盖不足
- 仍有 2 个 P2 缺陷未关闭，但已评估不阻塞上线

## Regression result
- 主流程回归通过
- 未发现 P0/P1 阻塞问题
- 核心功能可用
- 边界场景回归不充分

## Monitoring and rollback readiness
- 核心 API 监控已就绪
- 登录异常率看板已配置
- 通知成功率监控待最终确认
- 应用可快速回滚，数据库无结构变更，无需 DB 回滚
