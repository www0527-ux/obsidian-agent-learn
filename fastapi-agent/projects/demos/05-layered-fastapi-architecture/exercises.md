# Exercises

## 1. Explain The Request Flow
用自己的话解释：

```text
POST /users
-> app/api/routes/users.py
-> app/services/users.py
-> app/repositories/users.py
-> app/models/users.py
-> app/schemas/users.py
```

## 2. Exception Flow
解释这条链路中每一层的责任：

```text
IntegrityError
-> UserNameConflictError
-> HTTP 409
```

## 3. Boundary Debate
回答：

- `commit()` 应该在 repository 还是 service？
- `HTTPException` 能不能放在 service？
- `UserNotFoundError` 应该由 repository 抛，还是 service 抛？

## 4. Optional Refactor
实现一个全局 exception handler，让 router 不再手写 `try/except UserNameConflictError`。
