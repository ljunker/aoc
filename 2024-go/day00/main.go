package main

import (
	"aoc-go/util"
	_ "embed"
	"encoding"
	"flag"
	"fmt"
	"strings"
)

//go:embed input.txt
var input string

func init() {
	input = strings.TrimRight(input, "\n")
	if len(input) == 0 {
		panic("empty input.txt file")
	}
}

func main() {
	fmt.Printf("Part 1:")
	part1Timed := util.MeasureRuntime(part1)
	ans := part1Timed(input)
	fmt.Println("Output:", ans)
	err := util.CopyToClipboard(fmt.Sprintf("%v", ans))
	if err != nil {
		_ = fmt.Errorf("error running copytoclipboard %w", err)
	}
	fmt.Printf("Part 2:")
	part2Timed := util.MeasureRuntime(part2)
	ans = part2Timed(input)
	fmt.Println("Output:", ans)
	err = util.CopyToClipboard(fmt.Sprintf("%v", ans))
	if err != nil {
		_ = fmt.Errorf("error running copytoclipboard %w", err)
	}
}

func part1(input string) int {
	return 0
}

func part2(input string) int {

	return 0
}
