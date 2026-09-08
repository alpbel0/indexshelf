package com.indexshelf.app.core.network

import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Test
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.MockWebServer

class NetworkTransportTest {
    @Test fun productionRejectsCleartext() {
        assertThrows(IllegalArgumentException::class.java) {
            NetworkConfiguration("http://localhost/", production = true)
        }
    }

    @Test fun errorMapperReturnsStableDomainErrors() {
        assertEquals(NetworkError.Unauthorized, NetworkErrorMapper.map(401))
        assertEquals(NetworkError.Server, NetworkErrorMapper.map(503))
    }

    @Test fun interceptorAddsCorrelationAndIdempotencyHeaders() {
        val server = MockWebServer()
        server.enqueue(MockResponse().setResponseCode(204))
        server.start()
        val request = Request.Builder()
            .url(server.url("/jobs"))
            .post(ByteArray(0).toRequestBody())
            .build()
        val client = OkHttpClient.Builder()
            .addInterceptor(CorrelationIdInterceptor())
            .build()
        client.newCall(request).execute().use { response ->
            assertEquals(204, response.code)
        }
        val recorded = server.takeRequest()
        check(recorded.getHeader("X-Correlation-Id") != null)
        check(recorded.getHeader("Idempotency-Key") != null)
        server.shutdown()
    }
}
