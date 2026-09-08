package com.indexshelf.app.core.network

import java.util.UUID
import okhttp3.Interceptor
import okhttp3.Response

class CorrelationIdInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()
        val request = originalRequest.newBuilder()
            .header(
                "X-Correlation-Id",
                chain.request().header("X-Correlation-Id") ?: UUID.randomUUID().toString(),
            )
            .apply {
                if (originalRequest.method != "GET" && originalRequest.header("Idempotency-Key") == null) {
                    header("Idempotency-Key", UUID.randomUUID().toString())
                }
            }
            .header("X-Contract-Version", ApiContractVersion.MOBILE_V1)
            .build()
        return chain.proceed(request)
    }
}
