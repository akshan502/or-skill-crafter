# Tool Wrapper 模式完整示例

本文档展示 Tool Wrapper 模式的完整可运行示例：FastAPI 专家技能。

---

## 技能结构

```
skills/fastapi-expert/
├── SKILL.md                      # 路由指令 (< 100 行)
└── references/
    └── conventions.md            # FastAPI 完整规范 (500+ 行)
```

---

## SKILL.md

```markdown
---
name: fastapi-expert
description: FastAPI development best practices and conventions. Use when building, reviewing, or debugging FastAPI applications, REST APIs, Pydantic models, or async endpoints. Trigger keywords: fastapi, rest api, pydantic, async endpoint, dependency injection, api router.
metadata:
  pattern: tool-wrapper
  domain: fastapi
  depends_on:
    references:
      - conventions.md
---

# FastAPI Expert

You are an expert in FastAPI development. Apply these conventions to the user's code or question.

## When to Load Context

Load `references/conventions.md` when:
- User asks to write FastAPI code
- User submits code for review
- User asks about FastAPI best practices
- User debugs a FastAPI application

## Application Rules

### When Reviewing Code
1. Load `references/conventions.md`
2. Check each section of the user's code against relevant conventions
3. For each violation:
   - Cite the specific rule (section number from conventions)
   - Explain WHY it's problematic
   - Show corrected code

### When Writing Code
1. Load `references/conventions.md`
2. For each function/endpoint:
   - Use Annotated style for dependency injection
   - Add full type annotations
   - Include Pydantic models for input/output
   - Add appropriate HTTP status codes
3. Follow async patterns for database operations

### When Debugging
1. Load `references/conventions.md`
2. Identify common FastAPI issues:
   - Missing dependency injection
   - Incorrect async/await usage
   - Pydantic validation errors
   - Router configuration issues
3. Suggest fixes based on conventions

## Hard Constraints

- NEVER suggest synchronous code for database operations
- ALWAYS use Pydantic models for request/response bodies
- ALWAYS include error handling with proper HTTP status codes
```

---

## references/conventions.md (示例片段)

```markdown
# FastAPI Development Conventions

## 1. Dependency Injection

### 1.1 Use Annotated Style

**Rule**: Always use `Annotated` for dependency injection, not direct parameter injection.

```python
# ✓ Correct
from typing import Annotated
from fastapi import Depends

async def endpoint(
    db: Annotated[Database, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)]
):
    ...

# ✗ Wrong
async def endpoint(db: Database = Depends(get_db)):
    ...
```

**Reason**: Annotated style is clearer, more explicit, and works better with type checkers.

---

## 2. Type Annotations

### 2.1 Complete Return Types

**Rule**: Every endpoint must have a return type annotation.

```python
# ✓ Correct
@router.get("/users/{id}")
async def get_user(id: int) -> UserResponse:
    ...

# ✗ Wrong
@router.get("/users/{id}")
async def get_user(id: int):
    ...
```

---

## 3. Pydantic Models

### 3.1 Separate Input/Output Models

**Rule**: Use separate models for request body and response body.

```python
# ✓ Correct
class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

@router.post("/users")
async def create_user(data: UserCreate) -> UserResponse:
    ...
```

**Reason**: 
- Request model excludes auto-generated fields (id, timestamps)
- Response model can include computed fields
- Clear separation of what user can send vs what they receive

---

## 4. Async Patterns

### 4.1 Database Operations Must Be Async

**Rule**: All database I/O operations must use async/await.

```python
# ✓ Correct
async def get_user(db: Database, id: int):
    result = await db.query(User).filter_by(id=id).first()
    return result

# ✗ Wrong - will block the event loop
def get_user(db: Database, id: int):
    return db.query(User).filter_by(id=id).first()
```

---

## 5. Error Handling

### 5.1 Use HTTPException with Appropriate Status Codes

**Rule**: Raise HTTPException with the correct status code for error scenarios.

```python
from fastapi import HTTPException, status

# Not found
if user is None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

# Validation error
if not valid_email(email):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid email format"
    )

# Unauthorized
if not current_user.has_permission("admin"):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized"
    )
```

---

## 6. Router Organization

### 6.1 Use Router Prefixes

**Rule**: Group related endpoints under a router with prefix.

```python
# ✓ Correct
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")           # /users/
@router.get("/{id}")       # /users/{id}
@router.post("/")          # /users/
async def ...

# ✗ Wrong - no organization
@router.get("/users")
@router.get("/users/{id}")
@router.post("/users")
```
```

---

## 使用示例

### 用户触发

```
用户: "帮我写一个 FastAPI 的用户注册接口"
```

### Agent 行为

1. 检测到 "FastAPI" 关键词 → 触发 fastapi-expert 技能
2. 加载 `references/conventions.md`
3. 按照 convention 生成代码：
   - 使用 Annotated 依赖注入
   - 创建 UserCreate 和 UserResponse Pydantic 模型
   - 使用 async 函数
   - 包含适当的 HTTPException 处理

---

## 模式合规检查点

| 检查项 | 要求 |
|--------|------|
| 外部规范文件 | `references/conventions.md` 存在 |
| 动态加载指令 | SKILL.md 包含 "Load 'references/conventions.md'" |
| 无内联长规范 | SKILL.md < 100 行，规范在外部文件 |
| 按需加载说明 | 明确说明何时加载 (review/writing/debugging) |