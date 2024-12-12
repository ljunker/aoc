package main

import (
	"aoc-go/2024-go/util"
	_ "embed"
	"flag"
	"fmt"
	"image"
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
	flag.IntVar(&part, "part", 2, "part 1 or 2")
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

func makeGrid(input string) map[image.Point]rune {
	grid := map[image.Point]rune{}
	for y, s := range strings.Split(strings.TrimSpace(input), "\n") {
		for x, r := range s {
			grid[image.Point{X: x, Y: y}] = r
		}
	}
	return grid
}

func makeWords(point image.Point, length int, grid map[image.Point]rune) []string {
	delta := []image.Point{
		{-1, -1}, {1, -1}, {1, 1}, {-1, 1},
		{0, -1}, {1, 0}, {0, 1}, {-1, 0},
	}

	words := make([]string, len(delta))
	for i, d := range delta {
		for n := range length {
			words[i] += string(grid[point.Add(d.Mul(n))])
		}
	}
	return words
}

func part1(input string) int {
	grid := makeGrid(input)
	sum := 0
	for p := range grid {
		sum += strings.Count(strings.Join(makeWords(p, 4, grid), " "), "XMAS")
	}
	return sum
}

func part2(input string) int {
	grid := makeGrid(input)
	sum := 0
	for point := range grid {
		sum += strings.Count("AMAMASASAMAMAS", strings.Join(makeWords(point, 2, grid)[:4], ""))
	}
	return sum
}
