
import httpx

from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings


# Extract Bearer Token
bearer_scheme = HTTPBearer(auto_error=False)


# Authenticate Current User
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):

    # Check whether token exists
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = credentials.credentials

    # Verify token using Authentication Service
    try:

        async with httpx.AsyncClient(timeout=10.0) as client:

            response = await client.post(
                f"{settings.AUTH_SERVICE_URL.rstrip('/')}/api/auth/verify-token",
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )

        if response.status_code in (401, 403):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired authentication token",
                headers={"WWW-Authenticate": "Bearer"}
            )

        response.raise_for_status()

        result = response.json()

        if result.get("valid") is not True:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token verification failed",
                headers={"WWW-Authenticate": "Bearer"}
            )

        user_id = result.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user information in token"
            )

        return {
            "auth_user_id": int(user_id),
            "role": result.get("role")
        }

    except HTTPException:
        raise

    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication Service is unavailable"
        )

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication Service verification failed"
        )

    except (ValueError, TypeError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication response"
        )
