from flask import Flask, render_template, jsonify, request
from aiocoap import Context, Message, Code
import asyncio
import os

app = Flask(__name__)

DEVICE_HOST = os.environ.get('DEVICE_HOST', '192.168.1.100')
COAP_PORT = int(os.environ.get('COAP_PORT', 5683))

async def coap_get(resource):
    """Send a CoAP GET request to the ESP8266"""
    protocol = await Context.create_client_context()
    uri = f'coap://{DEVICE_HOST}:{COAP_PORT}/{resource}'

    request = Message(code=Code.GET, uri=uri)
    try:
        response = await protocol.request(request).response
        return response.payload.decode('utf-8')
    except Exception as e:
        print(f"Error in CoAP GET: {e}")
        return None

async def coap_post(resource, payload):
    """Send a CoAP POST request to the ESP8266"""
    protocol = await Context.create_client_context()
    uri = f'coap://{DEVICE_HOST}:{COAP_PORT}/{resource}'

    request = Message(code=Code.POST, uri=uri, payload=payload.encode('utf-8'))
    try:
        response = await protocol.request(request).response
        return response.payload.decode('utf-8')
    except Exception as e:
        print(f"Error in CoAP POST: {e}")
        return None

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', device_host=DEVICE_HOST)

@app.route('/device/led/state', methods=['GET'])
def get_led_status():
    """Get the current LED state from the device"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(coap_get('LED'))
        loop.close()

        if result:
            return jsonify({'result': 'ok', 'led': result})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to get LED status'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/device/led/action', methods=['POST'])
def control_led():
    """Control the LED on the device"""
    try:
        data = request.json
        command = data.get('command', '')

        if command not in ['On', 'Off']:
            return jsonify({'result': 'error', 'message': 'Invalid command'}), 400

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(coap_post('LED', command))
        loop.close()

        if result:
            return jsonify({'result': 'ok', 'message': result, 'led': command})
        else:
            return jsonify({'result': 'error', 'message': 'Failed to control LED'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/device/metrics/temperature', methods=['GET'])
def get_temperature():
    """Get temperature metric from the device"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(coap_get('temp'))
        loop.close()

        if result:
            try:
                temp_value = float(result)
                return jsonify({'result': 'ok', 'temperature_c': temp_value})
            except ValueError:
                return jsonify({'result': 'error', 'message': 'Invalid temperature value'}), 500
        else:
            return jsonify({'status': 'error', 'message': 'Failed to get temperature'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/device/metrics/tempvar', methods=['GET'])
def get_temp_var():
    """Get alternate temperature metric from the device"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(coap_get('tempVar'))
        loop.close()

        if result:
            try:
                temp_value = float(result)
                return jsonify({'result': 'ok', 'temperature_c': temp_value})
            except ValueError:
                return jsonify({'result': 'error', 'message': 'Invalid temperature value'}), 500
        else:
            return jsonify({'status': 'error', 'message': 'Failed to get temperature'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('APP_PORT', 8080)), debug=True)
