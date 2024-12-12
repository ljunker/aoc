package main

import (
	"aoc-go/util"
	_ "embed"
	"fmt"
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

type Pos struct {
	x, y int
}

const (
	E = 0
	S = 1
	W = 2
	N = 3
)

var directions = []Pos{
	E: {1, 0},
	S: {0, 1},
	W: {-1, 0},
	N: {0, -1},
}

func readGrid(input string) ([][]int, []Pos, []Pos) {
	var grid [][]int
	var starts, ends []Pos
	lines := strings.Split(input, "\n")
	for y, line := range lines {
		if line == "" {
			continue
		}
		var currentLine []int
		for x, ch := range line {
			num, _ := strconv.Atoi(string(ch))
			if num == 0 {
				starts = append(starts, Pos{x, y})
			}
			if num == 9 {
				ends = append(ends, Pos{x, y})
			}
			currentLine = append(currentLine, num)
		}
		grid = append(grid, currentLine)
	}
	return grid, starts, ends
}

func validMove(grid [][]int, start Pos, end Pos) bool {
	if end.x < 0 || end.x > len(grid[0])-1 || end.y < 0 || end.y > len(grid[0])-1 {
		return false
	}
	if grid[end.y][end.x]-grid[start.y][start.x] != 1 {
		return false
	}
	return true
}

func solve(grid [][]int, currentPos Pos, end Pos, visited map[Pos]bool, current []Pos, p2 bool) ([]Pos, int) {
	visited[currentPos] = true
	current = append(current, currentPos)
	var longest []Pos
	maxLength := 0
	if currentPos == end {
		if len(current) > len(longest) {
			longest = make([]Pos, len(current))
			copy(longest, current)
		}
		return longest, 1
	}

	var nextPos Pos
	for _, direction := range directions {
		nextPos.x = currentPos.x + direction.x
		nextPos.y = currentPos.y + direction.y
		if validMove(grid, currentPos, nextPos) {
			newPath, length := solve(grid, nextPos, end, visited, current, p2)

			longest = make([]Pos, len(current))
			copy(longest, newPath)
			if !p2 {
				if length > maxLength {
					maxLength = length
				}
			} else {
				maxLength += length
			}
		}
	}
	return longest, maxLength
}

func longest(grid [][]int, start Pos, end Pos, p2 bool) int {
	visited := make(map[Pos]bool)
	path := []Pos{}
	_, length := solve(grid, start, end, visited, path, p2)
	return length
}

func part1(input string) int {
	sum := 0
	grid, starts, ends := readGrid(input)
	for _, start := range starts {
		for _, end := range ends {
			sum += longest(grid, start, end, false)
		}
	}
	return sum
}

func part2(input string) int {
	sum := 0
	grid, starts, ends := readGrid(input)
	for _, start := range starts {
		for _, end := range ends {
			sum += longest(grid, start, end, true)
		}
	}
	return sum
}
