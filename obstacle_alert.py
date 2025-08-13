import time
import RPi.GPIO as GPIO

# === GPIO Pin Setup ===
TRIG = 4
ECHO = 17
MOTOR1 = 22  # May not work
MOTOR2 = 27  # Working motor

# === TIMING CONFIGURATION ===
MEASUREMENT_INTERVAL = 3.0  # seconds between measurements
ALERT_DURATION = 1.5        # seconds of vibration

# === DISTANCE ZONES (cm) ===
DISTANCE_ZONES = [
    (30, "🚨 DANGER",    "continuous", None, None),
    (100, "⚠️  WARNING",  "pulses", 0.1, 0.1),
    (200, "⚡ CAUTION",   "pulses", 0.2, 0.2),
    (400,"📡 DETECTION","pulses", 0.4, 0.5)
]

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(MOTOR1, GPIO.OUT)
GPIO.setup(MOTOR2, GPIO.OUT)
GPIO.output(TRIG, GPIO.LOW)
GPIO.output(MOTOR1, GPIO.LOW)
GPIO.output(MOTOR2, GPIO.LOW)

print("🔧 Testing motor...")
GPIO.output(MOTOR2, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(MOTOR2, GPIO.LOW)
print("✅ Motor test complete!")

# === Functions ===
def get_distance():
    """Get distance measurement in cm."""
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    start, stop = time.time(), time.time()
    timeout = time.time() + 0.1

    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        start = time.time()
    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        stop = time.time()

    elapsed = stop - start
    distance = (elapsed * 34300) / 2
    return distance

def vibrate(on_time, off_time, duration):
    """Pulse motor for a given pattern."""
    end_time = time.time() + duration
    while time.time() < end_time:
        GPIO.output(MOTOR2, GPIO.HIGH)
        time.sleep(on_time)
        GPIO.output(MOTOR2, GPIO.LOW)
        if off_time:
            time.sleep(off_time)

def give_alert(distance_cm, alert_duration):
    """Give feedback based on distance."""
    for limit, label, mode, on_t, off_t in DISTANCE_ZONES:
        if distance_cm < limit:
            print(f"{label} - Object at {distance_cm:.1f}cm")
            if mode == "continuous":
                GPIO.output(MOTOR2, GPIO.HIGH)
                time.sleep(alert_duration)
                GPIO.output(MOTOR2, GPIO.LOW)
            else:
                vibrate(on_t, off_t, alert_duration)
            return
    print(f"✅ ALL CLEAR - {distance_cm:.1f}cm")

def countdown(seconds):
    """Countdown to next measurement."""
    print("⏰ Next in: ", end="", flush=True)
    for i in range(int(seconds), 0, -1):
        print(f"{i}...", end="", flush=True)
        time.sleep(1)
    print("NOW!")

# === Main Program ===
print("\n🎯 TIMED PROXIMITY ALERT SYSTEM")
print("=" * 50)
for limit, label, mode, *_ in DISTANCE_ZONES:
    print(f"< {limit}cm: {label} ({mode})")
print("> 400cm: ✅ ALL CLEAR")
print("=" * 50)

print(f"\n🚀 Starting with {MEASUREMENT_INTERVAL}s intervals...")
print("Press Ctrl+C to exit\n")

measurement_count = 0
try:
    while True:
        measurement_count += 1
        print(f"\n[{measurement_count:03d}] 📏 Measuring...")
        dist = get_distance()
        give_alert(dist, ALERT_DURATION)

        wait_time = MEASUREMENT_INTERVAL - ALERT_DURATION
        if wait_time > 3:
            countdown(wait_time)
        elif wait_time > 0:
            time.sleep(wait_time)
except KeyboardInterrupt:
    print("\n🛑 Stopped by user.")
finally:
    GPIO.output(MOTOR1, GPIO.LOW)
    GPIO.output(MOTOR2, GPIO.LOW)
    GPIO.cleanup()
    print("✅ Cleanup complete.")
