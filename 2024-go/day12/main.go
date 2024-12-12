package main

import (
	"aoc-go/util"
	_ "embed"
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

func getGrid(input string) map[image.Point]rune {
	grid := map[image.Point]rune{}
	for y, s := range strings.Fields(string(input)) {
		for x, r := range s {
			grid[image.Point{x, y}] = r
		}
	}
	return grid
}

func floodFill(grid map[image.Point]rune) (int, int) {
	visited := map[image.Point]bool{}
	sum1 := 0
	sum2 := 0
	for p := range grid {
		if visited[p] {
			continue
		}
		visited[p] = true
		area := 1
		perimeter := 0
		sides := 0
		queue := []image.Point{p}
		for len(queue) > 0 {
			newPoint := queue[0]
			queue = queue[1:]

			for _, direction := range []image.Point{{0, -1}, {1, 0}, {0, 1}, {-1, 0}} {
				if neighbor := newPoint.Add(direction); grid[neighbor] != grid[newPoint] {
					perimeter++
					r := newPoint.Add(image.Point{-direction.Y, direction.X})
					if grid[r] != grid[newPoint] || grid[r.Add(direction)] == grid[newPoint] {
						sides++
					}
				} else if !visited[neighbor] {
					visited[neighbor] = true
					queue = append(queue, neighbor)
					area++
				}
			}
		}
		sum1 += perimeter * area
		sum2 += sides * area
	}
	return sum1, sum2
}

func part1(input string) int {
	grid := getGrid(input)
	sum1, _ := floodFill(grid)
	return sum1
}

func part2(input string) int {
	grid := getGrid(input)
	_, sum2 := floodFill(grid)
	return sum2
}
