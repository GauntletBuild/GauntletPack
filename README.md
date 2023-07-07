# Custom Blocks

```json
{
  "id": {
    "index": 0, // Indexes will always be increased no matter what
    "directions": {
      "NORTH": 1 // Each Direction will also increase the index, index increments are across blocks.
    }
  },
  "id2": {
    // As shown above indexes go forward including directions.
    "index": 2,
    "directions": {
      "SOUTH": 3
    }
  }
}
```

#### Note: You can open `number.html` to get the properties for your index to use in the block state.