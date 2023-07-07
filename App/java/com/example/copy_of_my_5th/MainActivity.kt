package com.example.copy_of_my_5th

import android.Manifest
import android.bluetooth.*
import android.bluetooth.le.BluetoothLeScanner
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanFilter
import android.bluetooth.le.ScanResult
import android.bluetooth.le.ScanSettings
import android.content.ContentValues.TAG
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.ListView
import android.widget.TextView
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.copy_of_my_5th.databinding.ActivityHomeBinding
import com.jjoe64.graphview.DefaultLabelFormatter
import com.jjoe64.graphview.series.DataPoint
import com.jjoe64.graphview.series.LineGraphSeries
import com.jjoe64.graphview.GraphView
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import android.util.Log
import com.google.gson.Gson
import java.lang.Double.max
import kotlinx.coroutines.*
import java.util.UUID
import com.google.gson.JsonObject
import okhttp3.sse.EventSource
import okhttp3.sse.EventSourceListener
import okhttp3.sse.EventSources


class SharedViewModel : ViewModel() {
    private val _Value1 = MutableLiveData<String>()
    val Value1: LiveData<String> get() = _Value1

    fun updateValue1(newValue: String) {
        _Value1.value = newValue
    }
}

class MainActivity : AppCompatActivity() {
    private val REQUEST_LOCATION_PERMISSION = 1
    private val REQUEST_ENABLE_BT = 2
    private val REQUEST_CODE_INTERNET_PERMISSION = 3
    private lateinit var bluetoothAdapter: BluetoothAdapter
    private lateinit var scanner: BluetoothLeScanner
    private lateinit var scanButton: Button
    private lateinit var resultTextView: TextView
    private lateinit var CurrentReadingValue_sys: TextView
    private var isConnected = false
    private lateinit var deviceListView: ListView
    private lateinit var deviceListAdapter: ArrayAdapter<String>
    private val deviceList: MutableList<String> = ArrayList()
    private val items: MutableList<BluetoothDevice> = mutableListOf()
    private var isScanning = false
    private var bluetoothGatt: BluetoothGatt? = null
    private lateinit var statusTextView: TextView
    private lateinit var deviceInfoTextView: TextView
    private lateinit var CurrentReadingValue_DIA: TextView
    private lateinit var current_reading_HEART_RATE_2: TextView
    private lateinit var disconnectButton: Button
    private val sharedViewModel: SharedViewModel by viewModels()
    private lateinit var context: Context

    private lateinit var binding: ActivityHomeBinding
    private lateinit var CurrentReadingValue: TextView

    private lateinit var handler: Handler
    private lateinit var runnable: Runnable

    private lateinit var graphView: GraphView
    private val series: LineGraphSeries<DataPoint> = LineGraphSeries()
    private var pointsAdded = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)


        scanButton = findViewById(R.id.scanButton)
        CurrentReadingValue = findViewById(R.id.CurrentReadingValue)
        deviceListView = findViewById(R.id.deviceListView)
        CurrentReadingValue_DIA = findViewById(R.id.CurrentReadingValue_DIA)
        current_reading_HEART_RATE_2 = findViewById(R.id.current_reading_HEART_RATE_2)
        deviceListAdapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, deviceList)
        deviceListView.adapter = deviceListAdapter
        context = applicationContext
        CurrentReadingValue_sys = findViewById(R.id.CurrentReadingValue_sys)

        val bluetoothManager = getSystemService(BLUETOOTH_SERVICE) as BluetoothManager
        bluetoothAdapter = bluetoothManager.adapter

        graphView = findViewById(R.id.graphView)

        graphView.addSeries(series)

        graphView.viewport.isXAxisBoundsManual = true
        graphView.viewport.isYAxisBoundsManual = true
        graphView.viewport.setMinX(0.0)
        graphView.viewport.setMaxX(3000.0)
        graphView.viewport.isScrollable = true
        graphView.gridLabelRenderer.isHorizontalLabelsVisible =
            false
        graphView.gridLabelRenderer.labelFormatter = object : DefaultLabelFormatter() {
            override fun formatLabel(value: Double, isValueX: Boolean): String {
                if (!isValueX) {
                    return if (value < 1000) "${value.toInt()}"
                    else "${(value / 1000).toInt()}k"
                } else {
                    return super.formatLabel(value, isValueX)
                }
            }
        }


        if (!isBluetoothEnabled()) {
            val enableBtIntent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
            startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT)
        }
        if (ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.INTERNET
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.INTERNET),
                REQUEST_CODE_INTERNET_PERMISSION
            )
        }

        scanner = bluetoothAdapter.bluetoothLeScanner

        scanButton.setOnClickListener {
            if (isConnected) {
                isConnected = false
                stopScan()
                scanButton.text = "Scan"
                CurrentReadingValue.text = "Received Random Number: "
            } else {
                if (hasLocationPermission()) {
                    if (isScanning) {
                        stopScan()
                    } else {
                        startScan()
                    }
                } else {
                    requestLocationPermission()
                }
            }
        }

        deviceListView.setOnItemClickListener { parent, view, position, id ->
            Toast.makeText(
                this, "Device Selected: " + deviceList[position], Toast.LENGTH_LONG
            ).show()

            val device = items[position]
            device.connectGatt(applicationContext, false, gattCallback)
        }

        statusTextView = findViewById(R.id.statusTextView)
        deviceInfoTextView = findViewById(R.id.deviceInfoTextView)
        disconnectButton = findViewById(R.id.disconnectButton)

        disconnectButton.setOnClickListener {
            bluetoothGatt?.disconnect()
        }

        startListeningForEvents()
    }

    override fun onResume() {
        super.onResume()
        if (bluetoothGatt != null && bluetoothAdapter.getProfileConnectionState(BluetoothProfile.GATT) == BluetoothProfile.STATE_CONNECTED) {
            statusTextView.text = "Connected"
            deviceInfoTextView.text =
                "Connected to ${bluetoothGatt?.device?.name ?: "Unknown"} ${bluetoothGatt?.device?.address}"
        }
    }

    private fun isBluetoothEnabled(): Boolean {
        return bluetoothAdapter.isEnabled
    }

    private fun hasLocationPermission(): Boolean {
        return ContextCompat.checkSelfPermission(
            applicationContext,
            Manifest.permission.ACCESS_FINE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED
    }

    private fun requestLocationPermission() {
        ActivityCompat.requestPermissions(
            this,
            arrayOf(Manifest.permission.ACCESS_FINE_LOCATION),
            REQUEST_LOCATION_PERMISSION
        )
    }

    private fun startScan() {
        val filters: MutableList<ScanFilter> = ArrayList()
        val settings = ScanSettings.Builder()
            .setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY)
            .build()

        scanner.startScan(filters, settings, scanCallback)
        isScanning = true
        scanButton.text = "Stop"
    }

    private fun stopScan() {
        scanner.stopScan(scanCallback)
        isScanning = false
        scanButton.text = "Scan"
        deviceList.clear()
        items.clear()
        deviceListAdapter.notifyDataSetChanged()
    }

    private val scanCallback: ScanCallback = object : ScanCallback() {
        override fun onScanResult(callbackType: Int, result: ScanResult) {
            super.onScanResult(callbackType, result)

            val device = result.device

            if (!items.contains(device)) {
                items.add(device)
                val deviceName = device.name ?: "Unknown Device"
                deviceList.add(deviceName + "\n" + device.address)
                deviceListAdapter.notifyDataSetChanged()
                // SO IF I DECOMMENT THIS TRIES TO CONNECT TO ALL DEVICES I Find     device.connectGatt(applicationContext, false, gattCallback)
            }
        }
    }

    private val gattCallback = object : BluetoothGattCallback() {
        override fun onConnectionStateChange(
            gatt: BluetoothGatt?,
            status: Int,
            newState: Int
        ) {
            super.onConnectionStateChange(gatt, status, newState)

            if (newState == BluetoothProfile.STATE_CONNECTED) {
                bluetoothGatt = gatt
                runOnUiThread {
                    scanButton.text = "Disconnect"
                    statusTextView.text = "Connected"
                    deviceInfoTextView.text =
                        "Connected to ${gatt?.device?.name ?: "Unknown"} ${gatt?.device?.address}"
                    Toast.makeText(
                        this@MainActivity,
                        "Connected to ${gatt?.device?.name}",
                        Toast.LENGTH_SHORT
                    ).show()
                }
                gatt?.discoverServices()
            } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                bluetoothGatt = null
                runOnUiThread {
                    scanButton.text = "Scan"
                    statusTextView.text = "Disconnected"
                    deviceInfoTextView.text = ""
                    Toast.makeText(
                        this@MainActivity,
                        "Disconnected from ${gatt?.device?.name}",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            }
        }

        override fun onServicesDiscovered(
            gatt: BluetoothGatt,
            status: Int
        ) {
            super.onServicesDiscovered(gatt, status)
            Log.d("GattCallback", "Services discovered, status: $status")

            if (status == BluetoothGatt.GATT_SUCCESS) {
                val serviceUUID =
                    UUID.fromString("9b6eb9d1-fe2f-4e24-8584-4c82e1ab4af2")
                val characteristicUUID =
                    UUID.fromString("483d59f3-40b7-4aa6-a6b1-fa145dfec8f7")

                val service = gatt.getService(serviceUUID)
                val characteristic = service.getCharacteristic(characteristicUUID)

                gatt.setCharacteristicNotification(characteristic, true)

                val descriptor =
                    characteristic.getDescriptor(UUID.fromString("00002902-0000-1000-8000-00805f9b34fb"))
                descriptor.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
                gatt.writeDescriptor(descriptor)
            }
        }

        override fun onCharacteristicRead(
            gatt: BluetoothGatt,
            characteristic: BluetoothGattCharacteristic,
            status: Int
        ) {
            super.onCharacteristicRead(gatt, characteristic, status)
            Log.d("GattCallback", "Characteristic read, status: $status")

            if (status == BluetoothGatt.GATT_SUCCESS) {
                val data = characteristic.getStringValue(0) // read string value

                runOnUiThread {
                    CurrentReadingValue.text = "Received Data: $data"
                }
            }
        }

        private val dataList = mutableListOf<String>()

        private var valueCounter = 0

        override fun onCharacteristicChanged(
            gatt: BluetoothGatt,
            characteristic: BluetoothGattCharacteristic
        ) {
            super.onCharacteristicChanged(gatt, characteristic)
            //  Log.d("GattCallback", "Characteristic changed: " + characteristic.uuid.toString())

            val data = characteristic.getStringValue(0)

            if (data != null) {
                runOnUiThread {
//                    val xValue = pointsAdded.toDouble()

                    CurrentReadingValue.text = data
                    Log.d("Value", data) // Log the value to the console

                    val dataValue = data.toDouble()
//                    series.appendData(DataPoint(xValue, dataValue), true, 100)
//
//                    pointsAdded += 1
//
//                    val range = 4000.0
//                    val minY = max(50000.0, dataValue - range / 2)
//                    val maxY = minY + range
//                    graphView.viewport.setMinY(minY)
//                    graphView.viewport.setMaxY(maxY)
//
//                    // Dynamically update X axis
//                    if (xValue >= 100) {
//                        graphView.viewport.setMinX(xValue - 100)
//                        graphView.viewport.setMaxX(xValue)
//                    }

                    valueCounter++

                    Log.d("Counter (Value Received)", valueCounter.toString())
                }
            }
        }
    }
    

    private fun processResponseData(data: String) {
        val jsonData = data.substringAfter("data:").trim()
        try {
            val response = Gson().fromJson(jsonData, JsonObject::class.java)

            val ppgValue = response["PPG"]?.asString ?: ""
            val sysValue = response["SYS"]?.asString ?: ""
            val diaValue = response["DIA"]?.asString ?: ""
            val heartRateValue = response["heartRate"]?.asString ?: ""

            runOnUiThread {

                CurrentReadingValue.text = ppgValue
                findViewById<TextView>(R.id.CurrentReadingValue_sys).text = sysValue
                findViewById<TextView>(R.id.CurrentReadingValue_DIA).text = diaValue
                findViewById<TextView>(R.id.current_reading_HEART_RATE_2).text = heartRateValue

                if (ppgValue.isNotEmpty()) {
                    val xValue = pointsAdded.toDouble()
                    val dataValue = ppgValue.toDouble()
                    series.appendData(DataPoint(xValue, dataValue), true, 100)

                    pointsAdded += 1

                    val range = 2250.0
                    val minY = max(50000.0, dataValue - range / 2)
                    val maxY = minY + range
                    graphView.viewport.setMinY(minY)
                    graphView.viewport.setMaxY(maxY)

                    if (xValue >= 100) {
                        graphView.viewport.setMinX(xValue - 100)
                        graphView.viewport.setMaxX(xValue)
                    }
                }
            }

            Log.d(TAG, "Response data: $data")
        } catch (e: Exception) {
            Log.e(TAG, "Error parsing event data: ${e.message}")
        }
    }


    private fun startListeningForEvents() {
        val client = OkHttpClient()
        val request = Request.Builder().url("http://146.169.186.128:8000/get_bp").build()

        val listener = object : EventSourceListener() {
            override fun onOpen(eventSource: EventSource, response: Response) {
                Log.d(TAG, "SSE connection opened")
            }

            override fun onEvent(
                eventSource: EventSource,
                id: String?,
                type: String?,
                data: String
            ) {
                Log.d(TAG, "New event received: $data")
                runOnUiThread {
                    processResponseData(data)
                }
            }

            override fun onClosed(eventSource: EventSource) {
                Log.d(TAG, "SSE connection closed")
                reconnectAfterDelay()
            }

            override fun onFailure(eventSource: EventSource, t: Throwable?, response: Response?) {
                Log.e(TAG, "SSE connection error: ${t?.message}")
                reconnectAfterDelay()
            }
        }

        EventSources.createFactory(client).newEventSource(request, listener)
    }

    private fun reconnectAfterDelay() {
        Handler(Looper.getMainLooper()).postDelayed({
            startListeningForEvents()
        }, 2000)  // Delay in milliseconds


    }
}




