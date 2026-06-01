package com.tuitionstation.app

import android.app.Application

class TuitionStationApp : Application() {
    override fun onCreate() {
        super.onCreate()
        instance = this
    }

    companion object {
        lateinit var instance: TuitionStationApp
            private set
    }
}
