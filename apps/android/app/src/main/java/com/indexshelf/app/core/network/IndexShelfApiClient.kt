package com.indexshelf.app.core.network

import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class IndexShelfApiClient(
    configuration: NetworkConfiguration,
    tokenStore: AccessTokenStore,
    refresher: TokenRefresher,
) {
    val retrofit: Retrofit = Retrofit.Builder()
        .baseUrl(configuration.baseUrl)
        .addConverterFactory(GsonConverterFactory.create())
        .client(
            OkHttpClient.Builder()
                .addInterceptor(CorrelationIdInterceptor())
                .addInterceptor(AuthInterceptor(tokenStore))
                .authenticator(TokenAuthenticator(tokenStore, refresher))
                .build(),
        ).build()
}
