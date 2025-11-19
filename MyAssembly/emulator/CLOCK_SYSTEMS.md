# Clock Systems - Three Approaches

The clock is the heartbeat of any computer. This module supports three different clock implementations, from pure software emulation to physical hardware.

## Overview

| Platform | Clock Source | Speed | Use Case |
|----------|--------------|-------|----------|
| **Dell Computer (Emulator)** | Software timing | Variable (0.1 Hz - 1 kHz) | Development, testing, debugging |
| **Arduino** | Hardware timer | 1 Hz - 16 MHz | Prototyping, semi-real hardware |
| **555 Timer (Breadboard)** | Astable multivibrator | 0.1 Hz - 10 Hz | Full hardware build, Ben Eater style |

---

## 1. Dell Computer Clock (Emulator Mode)

**How it works:**
- Uses Python's `time.time()` to measure elapsed time
- Software-controlled frequency from very slow (0.1 Hz) to fast (1 kHz)
- Perfect for development and debugging

**Advantages:**
- ✅ Variable speed - slow down to see each step
- ✅ Perfect timing accuracy
- ✅ No hardware required
- ✅ Pause, step, reset capabilities

**Example usage:**
```python
from emulator.clock import create_clock

# Create 1 Hz clock for visible stepping
clock = create_clock('emulator', 'slow')

# Or create fast clock for quick execution
clock = create_clock('emulator', 'turbo')  # 1 kHz

# Register callback for each clock cycle
def on_cycle():
    print("Executing instruction...")

clock.on_rising_edge(on_cycle)
clock.start()

# Clock runs in your main loop
while running:
    clock.tick()
    # Your CPU logic here
```

**Presets:**
- `'slow'`: 1 Hz - see each instruction
- `'normal'`: 10 Hz - comfortable speed
- `'fast'`: 100 Hz - quick execution
- `'turbo'`: 1000 Hz - maximum emulator speed

---

## 2. Arduino Clock

**How it works:**
- Uses Arduino's hardware timer interrupts (Timer1)
- Configurable frequency up to Arduino's crystal speed (16 MHz)
- More realistic than pure software, less complex than 555 timer

**Advantages:**
- ✅ Semi-real hardware experience
- ✅ More portable than breadboard
- ✅ Easy to reprogram and adjust
- ✅ Built-in debugging via Serial

**Arduino Sketch (excerpt):**
```cpp
// Timer1 interrupt for clock signal
ISR(TIMER1_COMPA_vect) {
    // Toggle clock pin
    digitalWrite(CLOCK_PIN, !digitalRead(CLOCK_PIN));
    
    // Execute next microcode step
    executeMicroStep();
}

void setup() {
    // Configure Timer1 for 1 Hz clock
    cli();  // Disable interrupts
    TCCR1A = 0;
    TCCR1B = 0;
    TCNT1 = 0;
    
    // 1 Hz: OCR1A = (16MHz / (1024 * 1Hz)) - 1 = 15624
    OCR1A = 15624;
    TCCR1B |= (1 << WGM12);  // CTC mode
    TCCR1B |= (1 << CS12) | (1 << CS10);  // 1024 prescaler
    TIMSK1 |= (1 << OCIE1A);  // Enable compare interrupt
    sei();  // Enable interrupts
}
```

**Timer frequency calculation:**
```
f_clock = f_cpu / (prescaler * (OCR1A + 1))

For 1 Hz with 16 MHz Arduino:
OCR1A = (16,000,000 / (1024 * 1)) - 1 = 15,624
```

---

## 3. 555 Timer Clock (Breadboard Hardware)

**How it works:**
- Physical 555 timer IC configured as astable multivibrator
- Frequency determined by resistor and capacitor values
- Generates square wave clock signal for physical hardware

**Advantages:**
- ✅ Pure hardware - no programming required
- ✅ Educational - see electronics in action
- ✅ Ben Eater style breadboard computer
- ✅ Real electrical engineering experience

### Circuit Design

**555 Timer in Astable Mode:**

```
        +5V
         |
         R1
         |
         +---- Threshold (Pin 6)
         |
         R2
         |
         +---- Trigger (Pin 2)
         |
         C
         |
        GND
```

**Frequency Formula:**
```
f = 1.44 / ((R1 + 2*R2) * C)
```

**Component Selection Examples:**

| Target Frequency | R1 | R2 | C | Actual Frequency |
|------------------|----|----|---|------------------|
| 0.5 Hz (slow) | 20kΩ | 20kΩ | 47µF | 0.50 Hz |
| 1 Hz (visible) | 48kΩ | 48kΩ | 10µF | 1.00 Hz |
| 10 Hz (fast) | 4.8kΩ | 4.8kΩ | 10µF | 10.00 Hz |

**Python design helper:**
```python
from emulator.clock import Timer555Emulator

# Design for target frequency
r1, r2 = Timer555Emulator.design_for_frequency(
    target_hz=1.0,
    c_farads=10e-6  # 10µF
)

print(f"Use R1={r1/1000:.1f}kΩ, R2={r2/1000:.1f}kΩ")
```

### Complete 555 Timer Circuit

```
Pin 1 (GND)     → Ground
Pin 2 (TRIG)    → Between R2 and C
Pin 3 (OUT)     → Clock signal to CPU
Pin 4 (RESET)   → +5V (or manual reset button)
Pin 5 (CTRL)    → 0.01µF to ground (noise filtering)
Pin 6 (THRESH)  → Between R1 and R2
Pin 7 (DISCH)   → Between R1 and R2
Pin 8 (VCC)     → +5V
```

**Bill of Materials (BOM):**
- 1× NE555 or LM555 timer IC
- 2× Resistors (20kΩ - 100kΩ depending on frequency)
- 1× Capacitor (10µF - 100µF electrolytic)
- 1× Capacitor (0.01µF ceramic, pin 5 noise filter)
- 1× LED + 330Ω resistor (optional, shows clock pulse)
- Breadboard and jumper wires

---

## Manual Stepping Mode (Debugging)

For ultimate control, use manual stepping:

```python
clock = create_clock('manual', 'slow')

# Execute one complete clock cycle
clock.step()  # Rising edge → falling edge

# Perfect for:
# - Single-stepping through programs
# - Debugging microcode
# - Understanding instruction execution
# - Classroom demonstrations
```

---

## Integration with CPU

The clock module integrates with the CPU emulator:

```python
from emulator.clock import create_clock
from emulator.cpu import CPU

# Create CPU and clock
cpu = CPU()
clock = create_clock('emulator', 'normal')

# Connect clock to CPU
clock.on_rising_edge(cpu.fetch)     # Fetch on rising edge
clock.on_falling_edge(cpu.execute)  # Execute on falling edge

# Run the computer
clock.start()
while cpu.running:
    clock.tick()
```

---

## Clock Speed Recommendations

**Development Phase:**
- Use `'slow'` (1 Hz) to watch each instruction
- Use `'manual'` mode to single-step through programs

**Testing Phase:**
- Use `'normal'` (10 Hz) for comfortable execution speed
- Use `'fast'` (100 Hz) when testing longer programs

**Production Phase:**
- Use `'turbo'` (1 kHz) for maximum emulator performance
- Use Arduino with 1-100 Hz for hardware prototype
- Use 555 timer at 0.5-1 Hz for breadboard build (visible LEDs)

**Hardware Build:**
- Start with 0.5 Hz - you can see LEDs change state
- Increase to 1-2 Hz once everything works
- Ben Eater's computer runs at ~600 Hz for visible yet practical speed

---

## Philosophy

The clock demonstrates the **abstraction ladder** from pure software to pure hardware:

1. **Emulator (Dell Computer)**: Pure software, perfect control
2. **Arduino**: Software + hardware timer, realistic simulation  
3. **555 Timer**: Pure hardware, real electrical engineering

All three use the **same CPU design and microcode**, proving that:
- Hardware and software are fundamentally equivalent
- Good abstraction allows platform independence
- Understanding spans from bits to breadboards

This mirrors the nandCompute philosophy: **build from first principles, understand every layer**.

---

## Next Steps

- [x] Clock module implemented
- [ ] CPU emulator with clock integration
- [ ] Arduino sketch with Timer1 configuration
- [ ] 555 timer breadboard schematic
- [ ] PCB design (optional, advanced)

The clock is ready. Now let's build the CPU that runs on it!
