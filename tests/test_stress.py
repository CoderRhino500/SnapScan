import pytest
import time
import os
import psutil
from PIL import Image
import random
from snapscan_core import Scanner

# Test 1: The Rapid-Fire Load Test
def test_rapid_fire_scanning():
    """
    Simulates a user mashing the hotkey or a kiosk app scanning continuously.
    Verifies that the library can handle 50 rapid back-to-back screen captures 
    without throwing OS-level thread or screen locking errors.
    """
    scanner = Scanner()
    success_count = 0
    
    start_time = time.time()
    for _ in range(50):
        # We don't care if it finds a QR code, just that it doesn't crash
        result = scanner.scan() 
        assert result is not None  # Must always return a ScanResult
        success_count += 1
        
    end_time = time.time()
    
    # Ensure all 50 scans completed
    assert success_count == 50
    print(f"\nCompleted 50 rapid scans in {end_time - start_time:.2f} seconds.")

# Test 2: The Memory Leak Test
def test_memory_leaks():
    """
    Capturing images can quickly fill up RAM if variables aren't cleared.
    This test runs 100 captures and monitors the system's memory usage 
    to ensure the PIL images are being successfully garbage collected.
    """
    scanner = Scanner()
    process = psutil.Process(os.getpid())
    
    # Record baseline memory usage
    initial_memory = process.memory_info().rss / (1024 * 1024) # In MB
    
    for _ in range(100):
        _ = scanner.scan()
        
    # Record final memory usage
    final_memory = process.memory_info().rss / (1024 * 1024)
    
    memory_growth = final_memory - initial_memory
    print(f"\nMemory growth after 100 scans: {memory_growth:.2f} MB")
    
    # The growth should be minimal (allow a small buffer for Python overhead, e.g., < 20MB)
    assert memory_growth < 20.0, "Memory leak detected: RAM usage grew too much!"

# Test 3: The Garbage Data Test
def test_garbage_image_handling():
    """
    Simulates a developer passing corrupted, microscopic, or pure noise images
    directly into the scan_image() method to ensure pyzbar doesn't crash.
    """
    scanner = Scanner()
    
    # Generate an image of pure random static noise
    random_pixels = bytes([random.randint(0, 255) for _ in range(100 * 100 * 3)])
    noise_image = Image.frombytes("RGB", (100, 100), random_pixels)
    
    # Generate an impossibly small image (1x1 pixel)
    tiny_image = Image.new("RGB", (1, 1), color="white")
    
    # The decoder MUST NOT crash. It must elegantly return ScanResult(found=False).
    noise_result = scanner.scan_image(noise_image)
    assert noise_result.found is False
    
    tiny_result = scanner.scan_image(tiny_image)
    assert tiny_result.found is False