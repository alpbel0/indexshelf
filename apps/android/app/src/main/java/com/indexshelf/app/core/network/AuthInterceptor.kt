package com.indexshelf.app.core.network

import okhttp3.Interceptor
import okhttp3.Response

fun interface AccessTokenStore { fun accessToken(): String? }

class AuthInterceptor(private val tokenStore: AccessTokenStore) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val token = tokenStore.accessToken()
        val request = chain.request().newBuilder().apply {
            if (!token.isNullOrBlank()) header("Authorization", "Bearer $token")
        }.build()
        return chain.proceed(request)
    }
}
