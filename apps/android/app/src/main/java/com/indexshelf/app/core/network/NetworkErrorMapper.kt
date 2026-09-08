package com.indexshelf.app.core.network

sealed interface NetworkError {
    data object Offline : NetworkError
    data object Unauthorized : NetworkError
    data object Forbidden : NetworkError
    data object InvalidRequest : NetworkError
    data object Conflict : NetworkError
    data object RateLimited : NetworkError
    data object Server : NetworkError
    data class Unknown(val code: Int) : NetworkError
}

object NetworkErrorMapper {
    fun map(code: Int): NetworkError = when {
        code == 401 -> NetworkError.Unauthorized
        code in 500..599 -> NetworkError.Server
        code == 0 -> NetworkError.Offline
        else -> NetworkError.Unknown(code)
    }

    fun map(code: Int, problemType: String?, errorCode: String?): NetworkError {
        val contractCode = errorCode ?: problemType?.substringAfterLast('/')
        return when (contractCode) {
            "common.unauthorized", "unauthorized" -> NetworkError.Unauthorized
            "common.forbidden", "forbidden" -> NetworkError.Forbidden
            "common.invalid_request", "invalid-request" -> NetworkError.InvalidRequest
            "common.conflict", "conflict" -> NetworkError.Conflict
            "common.rate_limited", "rate-limited" -> NetworkError.RateLimited
            else -> map(code)
        }
    }
}
