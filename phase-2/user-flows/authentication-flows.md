# Phase II - Authentication User Flows

## Flow 1: User Signup

```
┌─────────────────────────────────────────────────────────────────────┐
│ SIGNUP PAGE (/signup)                                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Evolution of Todo                                          │   │
│  │  Create your account to start managing tasks                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Email                                                      │   │
│  │  [ user@example.com                        ]                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Password (minimum 8 characters)                            │   │
│  │  [ *******************                      ]                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  [ Create Account ]                                         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Already have an account? [Sign in]                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

Success Path:
1. User enters valid email and 8+ char password
2. Clicks "Create Account"
3. Loading spinner appears
4. On success: Redirect to /todos
5. User sees their todo list

Error Path - Duplicate Email:
1. User enters existing email
2. Clicks "Create Account"
3. Error displayed: "An account with this email already exists"

Error Path - Invalid Email:
1. User enters invalid email format
2. Clicks "Create Account"
3. Error displayed: "Please enter a valid email address"

Error Path - Weak Password:
1. User enters password < 8 characters
2. Clicks "Create Account"
3. Error displayed: "Password must be at least 8 characters"
```

---

## Flow 2: User Signin

```
┌─────────────────────────────────────────────────────────────────────┐
│ SIGNIN PAGE (/signin)                                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Welcome back!                                              │   │
│  │  Sign in to access your todos                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Email                                                      │   │
│  │  [ user@example.com                        ]                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Password                                                   │   │
│  │  [ *******************                      ]                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  [ Sign In ]                                                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Don't have an account? [Sign up]                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

Success Path:
1. User enters correct credentials
2. Clicks "Sign In"
3. Loading spinner appears
4. On success: Redirect to /todos
5. User sees their todo list

Error Path - Invalid Credentials:
1. User enters wrong email or password
2. Clicks "Sign In"
3. Error displayed: "Invalid email or password"

Validation Path:
1. User leaves email/password empty
2. Clicks "Sign In"
3. Inline validation: "Email is required", "Password is required"
```

---

## Flow 3: Protected Route Access

```
Unauthenticated User Navigates to /todos:

┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  User enters URL: https://app.example.com/todos                     │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  AuthGuard checks session                                   │   │
│  │  Session: None / Invalid                                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                     │
│                              ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Redirect to /signin                                        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                     │
│                              ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  User sees signin page                                      │   │
│  │  Optional: "Please sign in to access your todos" message   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Flow 4: User Signout

```
Authenticated User on Any Page:

┌─────────────────────────────────────────────────────────────────────┐
│ HEADER                                                              │
│ ┌─────────────────────────────────────────────────────────────┐    │
│ │ Evolution of Todo  |  user@example.com  [Sign out]         │    │
│ └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘

Signout Flow:
1. User clicks "Sign out" button
2. API call: POST /api/auth/signout
3. Session deleted from database
4. Session cookie cleared
5. Redirect to /signin

Post-Signout:
- User cannot access /todos
- User cannot make API requests
- User sees signin page when navigating to protected routes
```

---

## Flow 5: Session Expiration

```
Authenticated User with Expired Session:

1. User's session expires (e.g., 7 days of inactivity)
2. User attempts API request
3. API returns: 401 Unauthorized

┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  API Request: GET /api/todos                                │   │
│  │  Headers: { Cookie: better-auth.session_token=... }        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                     │
│                              ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Response: 401 Unauthorized                                 │   │
│  │  Body: { error: "Session expired. Please sign in again." } │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                     │
│                              ▼                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Frontend handles 401:                                      │   │
│  │  - Clear local auth state                                   │   │
│  │  - Redirect to /signin                                      │   │
│  │  - Show toast: "Your session expired. Please sign in."     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Flow 6: Multi-Device Session

```
User Signs In on Multiple Devices:

Device 1 (Laptop):
┌─────────────────────────────────────────┐
│  Browser A - Signed in as user@example.com  │
└─────────────────────────────────────────┘

Device 2 (Phone):
┌─────────────────────────────────────────┐
│  Browser B - Signs in as user@example.com  │
│  → New session created in database      │
└─────────────────────────────────────────┘

Result:
- Both sessions are valid
- Each device has its own session token
- Sign out on one device only ends that session
- No "force logout" on other devices (per spec)

Conflict (if implemented):
- Last signin wins
- Earlier session invalidated
```

---

## Validation Rules

### Email Validation
| Rule | Regex | Example |
|------|-------|---------|
| Format | `^[^@\s]+@[^@\s]+\.[^@\s]+$` | user@example.com |
| Max length | 255 characters | - |
| Case sensitivity | Stored lowercase for uniqueness | User@Example.com = user@example.com |

### Password Validation
| Rule | Requirement |
|------|-------------|
| Minimum length | 8 characters |
| Storage | bcrypt hash (cost factor 12) |
| Plaintext | Never stored |

### Session Validation
| Rule | Requirement |
|------|-------------|
| Expiration | Configurable (default: 7 days) |
| Cookie | HTTP-only, Secure (production), SameSite=Lax |
| Refresh | Automatic on activity |

---

## Error Messages

| Scenario | Message |
|----------|---------|
| Invalid email format | "Please enter a valid email address" |
| Email already exists | "An account with this email already exists" |
| Password too short | "Password must be at least 8 characters" |
| Invalid credentials | "Invalid email or password" |
| Email required | "Email is required" |
| Password required | "Password is required" |
| Session expired | "Your session has expired. Please sign in again." |
| Not authenticated | "Please sign in to access this page." |
