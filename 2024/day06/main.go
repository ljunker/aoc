package main

import (
	"aoc-go/util"
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

type thing struct {
	dir        image.Point
	loc        image.Point
	isObstacle bool
	isGuard    bool
	wasVisited bool
}

func makeGrid(input string) (map[image.Point]thing, thing, int, int) {
	grid := map[image.Point]thing{}
	var guard thing
	width := 0
	height := 0
	for y, s := range strings.Split(input, "\n") {
		width = len(s)
		height = y
		for x, r := range s {
			var current thing
			if r == '^' {
				current.isObstacle = false
				current.wasVisited = true
				current.isGuard = false
				guard.isGuard = true
				guard.dir = image.Point{0, -1}
				guard.loc = image.Point{x, y}
			} else if r == '#' {
				current.isGuard = false
				current.isObstacle = true
				current.wasVisited = false
			} else {
				current.isObstacle = false
				current.wasVisited = false
				current.isGuard = false
			}
			grid[image.Point{X: x, Y: y}] = current
		}
	}
	return grid, guard, width, height
}

func offGrounds(guard thing, width int, height int) bool {
	return guard.loc.X < 0 || guard.loc.X >= width || guard.loc.Y < 0 || guard.loc.Y >= height
}

func obstacleInFront(guard thing, grid map[image.Point]thing, width int, height int) bool {
	possObs := guard.loc.Add(guard.dir)
	if possObs.X < 0 || possObs.Y < 0 || possObs.X >= width || possObs.Y >= height {
		return false
	}
	return grid[possObs].isObstacle
}

func turn90Degrees(guard *thing) {
	tempX := guard.dir.X
	tempY := guard.dir.Y
	guard.dir.Y = tempX
	guard.dir.X = tempY * -1
}

func takeStepForward(guard *thing) {
	guard.loc = guard.loc.Add(guard.dir)
}

func part1(input string) int {
	grid, guard, width, height := makeGrid(input)
	height++
	s := map[image.Point]bool{}
	drawGrid(s, guard, grid, width, height)
	for !offGrounds(guard, width, height) {
		if obstacleInFront(guard, grid, width, height) {
			turn90Degrees(&guard)
		} else {
			s[guard.loc] = true
			takeStepForward(&guard)
		}
	}
	drawGrid(s, guard, grid, width, height)
	return len(s)
}

func drawGrid(s map[image.Point]bool, guard thing, grid map[image.Point]thing, width int, height int) {
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			t := grid[image.Point{x, y}]
			c := "."
			if x == guard.loc.X && y == guard.loc.Y {
				c = "G"
			}
			if t.isObstacle {
				c = "#"
			}
			if s[image.Point{x, y}] {
				c = "X"
			}
			fmt.Printf("%s", c)
		}
		fmt.Println()
	}
	fmt.Println("-----------------------")
}

type locationAndDirection struct {
	loc image.Point
	dir image.Point
}

func part2(input string) int {
	grid, guard, width, height := makeGrid(input)
	maxWidth, maxHeight := width, height
	maxHeight++
	height++
	positions := 0
	for y := 0; y < maxHeight; y++ {
		for x := 0; x < maxWidth; x++ {
			grid, guard, width, height = makeGrid(input)
			height++
			current := thing{isObstacle: true}
			grid[image.Point{X: x, Y: y}] = current
			s := map[locationAndDirection]bool{}
			for !offGrounds(guard, width, height) {
				if obstacleInFront(guard, grid, width, height) {
					turn90Degrees(&guard)
				} else {
					var loc locationAndDirection
					loc.loc = guard.loc
					loc.dir = guard.dir
					if s[loc] {
						//loop detected
						positions++
						//drawGrid(make(map[image.Point]bool), guard, grid, width, height)
						break
					}
					s[loc] = true
					takeStepForward(&guard)
				}
			}
		}
	}
	return positions
}
