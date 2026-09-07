package com.indexshelf.app

import com.indexshelf.app.R
import org.junit.Assert.assertEquals
import org.junit.Test

class StartupTest {
    @Test
    fun startupStateHasWelcomeMessage() {
        assertEquals(R.string.startup_welcome, StartupState.WelcomeMessage)
    }
}
