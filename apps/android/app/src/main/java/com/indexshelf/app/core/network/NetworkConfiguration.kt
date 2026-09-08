package com.indexshelf.app.core.network

data class NetworkConfiguration(val baseUrl: String, val production: Boolean) {
    init {
        require(baseUrl.endsWith("/")) { "baseUrl must end with /" }
        if (production) require(baseUrl.startsWith("https://")) { "Production API must use HTTPS" }
    }
}
