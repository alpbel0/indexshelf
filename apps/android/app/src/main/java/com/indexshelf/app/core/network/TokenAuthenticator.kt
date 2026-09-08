package com.indexshelf.app.core.network

import java.util.concurrent.locks.ReentrantLock
import okhttp3.Authenticator
import okhttp3.Request
import okhttp3.Response
import okhttp3.Route

fun interface TokenRefresher { fun refresh(): String? }

@Suppress("ReturnCount")
class TokenAuthenticator(
    private val tokenStore: AccessTokenStore,
    private val refresher: TokenRefresher,
) : Authenticator {
    private val lock = ReentrantLock()
    override fun authenticate(route: Route?, response: Response): Request? {
        if (responseCount(response) >= 2) return null
        lock.lock()
        try {
            val current = tokenStore.accessToken()
            if (current != null && response.request.header("Authorization")?.endsWith(current) == false) {
                return response.request.newBuilder()
                    .header("Authorization", "Bearer $current").build()
            }
            val refreshed = refresher.refresh() ?: return null
            return response.request.newBuilder().header("Authorization", "Bearer $refreshed").build()
        } finally { lock.unlock() }
    }
    private fun responseCount(response: Response): Int {
        var count = 1
        var prior = response.priorResponse
        while (prior != null) { count++; prior = prior.priorResponse }
        return count
    }
}
