package util

import (
	"fmt"
	"time"
)

func MeasureRuntime[A any, R any](fn func(A) R) func(A) R {
	return func(arg A) R {
		start := time.Now()
		result := fn(arg)
		elapsed := time.Since(start)
		fmt.Println("elapsed:", elapsed)
		return result
	}
}
