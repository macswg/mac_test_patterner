# Half Tile Placement System

## Overview
The code now supports flexible half-tile placement using a numeric system in the `half tile top` field.

## Usage

### Numeric Position Values
- **0** = Half tile at the **top**
- **1** = Half tile after the **1st row**
- **2** = Half tile after the **2nd row**
- **3** = Half tile after the **3rd row**
- ...and so on...
- **99** = Half tile at the **bottom** (default)

### Example Configuration

```json
{
  "panels wide": 10,
  "panels high": 4.5,
  "half tile top": "0"
}
```
This places the half tile row at the top.

```json
{
  "panels wide": 10,
  "panels high": 4.5,
  "half tile top": "2"
}
```
This places the half tile row after the 2nd full row.

```json
{
  "panels wide": 10,
  "panels high": 4.5,
  "half tile top": "99"
}
```
This places the half tile row at the bottom (default behavior).

## Technical Details

### Changes Made

1. **`parse_half_tile_position()` function**: Replaces the old `half_tile_top_bool()` function. Converts the input to an integer position value.

2. **`half_tile_position` variable**: Stores the numeric position (0-99) instead of a boolean.

3. **Dynamic Y-position calculation**: `half_tile_y_position` is calculated based on the position value:
   - Position 0: Top of canvas
   - Position 1-98: After that row number
   - Position 99+: Bottom of canvas

4. **Smart tile drawing**: The tile drawing logic now handles three cases:
   - **Position 0 (top)**: All full tiles are shifted down by half a tile height
   - **Position 1-98 (middle)**: Full tiles above the half tile draw normally, full tiles below are shifted down by half a tile height
   - **Position 99 (bottom)**: All full tiles draw normally at the top

5. **Text positioning**: Panel index numbers are automatically adjusted based on where the half tile is inserted.

6. **Checkerboard pattern preservation**: The alternating color pattern is maintained regardless of where the half tile is placed.

## Tile Numbering System

The tile numbers are adjusted based on where the half tile is placed:

### Position 0 (Top)
- Half tile row = **1**
- Full tiles below = **2, 3, 4, 5...**

Example with 4.5 panels high:
```
Row 1 (half tile)
Row 2 (full tile)
Row 3 (full tile)
Row 4 (full tile)
Row 5 (full tile)
```

### Position 1-98 (Middle)
- Full tiles above = **1, 2, 3...**
- Half tile row = **N+1** (where N is the position value)
- Full tiles below = **N+2, N+3...**

Example with position 2 and 4.5 panels high:
```
Row 1 (full tile)
Row 2 (full tile)
Row 3 (half tile) ← after row 2
Row 4 (full tile)
Row 5 (full tile)
```

### Position 99 (Bottom)
- Full tiles above = **1, 2, 3, 4...**
- Half tile row = **N+1** (after last full tile)

Example with 4.5 panels high:
```
Row 1 (full tile)
Row 2 (full tile)
Row 3 (full tile)
Row 4 (full tile)
Row 5 (half tile)
```

## Backward Compatibility

If an invalid value is provided, the system defaults to position 99 (bottom), maintaining the most common use case.

