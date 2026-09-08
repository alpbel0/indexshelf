package com.indexshelf.app.core.network

import android.content.Context
import android.net.ConnectivityManager
import android.net.NetworkCapabilities

class ConnectivityObserver(context: Context) {
    private val manager = context.getSystemService(ConnectivityManager::class.java)
    fun isOnline(): Boolean = manager.activeNetwork?.let {
        manager.getNetworkCapabilities(it)
            ?.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
    } == true
}
