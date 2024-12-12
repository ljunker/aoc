package main

import (
	"aoc-go/util"
	_ "embed"
	"flag"
	"fmt"
	"regexp"
	"strconv"
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
	var part int
	flag.IntVar(&part, "part", 1, "part 1 or 2")
	flag.Parse()
	fmt.Println("Running part", part)

	if part == 1 {
		part1Timed := util.MeasureRuntime(part1)
		ans := part1Timed(input)
		fmt.Println("Output:", ans)
		err := util.CopyToClipboard(fmt.Sprintf("%v", ans))
		if err != nil {
			_ = fmt.Errorf("error running copytoclipboard %w", err)
		}
	} else {
		part2Timed := util.MeasureRuntime(part2)
		ans := part2Timed(input)
		fmt.Println("Output:", ans)
		err := util.CopyToClipboard(fmt.Sprintf("%v", ans))
		if err != nil {
			_ = fmt.Errorf("error running copytoclipboard %w", err)
		}
	}
}

func part1(input string) int {
	re := regexp.MustCompile(`mul\((\d+),(\d+)\)`)
	sum := 0
	matches := re.FindAllStringSubmatch(input, -1)
	for _, match := range matches {
		if len(match) == 3 {
			a, err1 := strconv.Atoi(match[1])
			b, err2 := strconv.Atoi(match[2])
			if err1 == nil && err2 == nil {
				sum += a * b
			}
		}
	}
	return sum
}

func part2(input string) int {
	re := regexp.MustCompile(`mul\((\d+),(\d+)\)|do\(\)|don't\(\)`)
	sum := 0
	do := true
	matches := re.FindAllStringSubmatch(input, -1)
	for _, match := range matches {
		if match[0] == "don't()" {
			do = false
		} else if match[0] == "do()" {
			do = true
		} else if do {
			a, err1 := strconv.Atoi(match[1])
			b, err2 := strconv.Atoi(match[2])
			if err1 == nil && err2 == nil {
				sum += a * b
			}
		}
	}
	return sum
}
