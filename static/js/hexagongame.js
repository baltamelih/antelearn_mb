// number of rows and minimum number of columns, you can adjust as you please
let n_rows = 3; // at least 1 !!!
let n_cols_min = 2; // at least 1 !!!

// image urls, you can replace with your own


let n_cols_max = n_cols_min + 1, n_cols_sum = n_cols_max + n_cols_min;
let n = Math.ceil(.5*n_rows)*n_cols_min + Math.floor(.5*n_rows)*n_cols_max;
let ni = imgs.length;

body(style=`--n-rows: ${n_rows}; --n-cols: ${2*n_cols_max}`)
  style.hex-cell:nth-of-type(#{n_cols_sum}n + 1); { grid-column-start: 2 };
