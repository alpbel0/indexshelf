package com.indexshelf.contracts.smoke

import com.indexshelf.contracts.generated.models.CursorPage
import com.indexshelf.contracts.generated.models.ProblemDetails

fun main() {
    check(CursorPage::class.java.simpleName == "CursorPage")
    check(ProblemDetails::class.java.simpleName == "ProblemDetails")
}
