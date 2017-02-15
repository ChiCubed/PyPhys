# PyPhys
A physics library for Python.
#### Complexity
| Preprocessing |     Query     |   Update   |
| :-----------: |     :---:     |   :----:   |
| `O(N)`        | `O(inverse)`* |   `O(N)`   |
&ast;`inverse` is the cost of performing the inverse of whatever function you have chosen to perform. For example, if you have a prefix sum array using multiplication, the cost of the inverse would be the cost of division.

#### Pseudocode
```
func preprocess takes an array arr as input:
  Create a new array pre with the same
  length as the original

  pre[0] = arr[0]
  For i in 1 to the length```
