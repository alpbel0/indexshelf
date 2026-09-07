package com.indexshelf.app

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithText
import org.junit.Rule
import org.junit.Test

class StartupComposeTest {
    @get:Rule
    val composeRule = createComposeRule()

    @Test
    fun startupMessageIsDisplayed() {
        composeRule.setContent { IndexShelfStartup() }
        composeRule.onNodeWithText(StartupState.WelcomeMessage).assertIsDisplayed()
    }
}
