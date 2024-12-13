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

func makeAntennas(input string) (map[rune][]image.Point, int, int) {
	antennas := map[rune][]image.Point{}
	width := 0
	height := 0
	split := strings.Split(input, "\n")
	width = len(split[0])
	height = len(split)
	for y, s := range split {
		for x, r := range s {
			if r == '.' {
				continue
			}
			if _, exists := antennas[r]; !exists {
				antennas[r] = []image.Point{}
			}
			antennas[r] = append(antennas[r], image.Point{x, y})
		}
	}
	return antennas, width, height
}

func part1(input string) int {
	antennas, width, height := makeAntennas(input)
	var listOfAllAntinodes []image.Point
	var nodesList [][]image.Point
	for _, listOnFrequency := range antennas {
		for i := 0; i < len(listOnFrequency); i++ {
			for j := i + 1; j < len(listOnFrequency); j++ {
				points := countAntinodes(listOnFrequency[i], listOnFrequency[j], width, height)
				listOfAllAntinodes = unionPoints(listOfAllAntinodes, points)
				nodesList = append(nodesList, points)
			}
		}
	}
	drawGrid(antennas, nodesList, width, height)
	return len(listOfAllAntinodes)
}

func unionPoints(a []image.Point, b []image.Point) []image.Point {
	pointMap := make(map[image.Point]struct{})

	for _, point := range a {
		pointMap[point] = struct{}{}
	}
	for _, point := range b {
		pointMap[point] = struct{}{}
	}

	union := make([]image.Point, 0, len(pointMap))
	for point := range pointMap {
		union = append(union, point)
	}
	return union
}

func drawGrid(antennas map[rune][]image.Point, list [][]image.Point, width int, height int) {
	grid := map[image.Point]rune{}
	for x, points := range antennas {
		for _, point := range points {
			grid[point] = x
		}
	}
	for _, nodeList := range list {
		for _, node := range nodeList {
			grid[node] = '#'
		}
	}
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			if val, _ := grid[image.Point{x, y}]; val != 0 {
				fmt.Printf("%c", val)
			} else {
				fmt.Print(".")
			}
		}
		fmt.Println()
	}
}

func countAntinodes(a image.Point, b image.Point, width int, height int) []image.Point {
	var nodes []image.Point
	n1 := image.Point{
		X: (b.X-a.X)*2 + a.X,
		Y: (b.Y-a.Y)*2 + a.Y,
	}
	n2 := image.Point{
		X: (a.X-b.X)*2 + b.X,
		Y: (a.Y-b.Y)*2 + b.Y,
	}
	if n1.X >= 0 && n1.X < width && n1.Y >= 0 && n1.Y < height {
		nodes = append(nodes, n1)
	}
	if n2.X >= 0 && n2.X < width && n2.Y >= 0 && n2.Y < height {
		nodes = append(nodes, n2)
	}
	return nodes
}

func countAntinodesPart2(a image.Point, b image.Point, width int, height int) []image.Point {
	var nodes []image.Point
	distance := image.Point{b.X - a.X, b.Y - a.Y}
	n := image.Point{0, 0}
	i := 0
	for n.X >= 0 && n.X < width && n.Y >= 0 && n.Y < height {
		n = b.Add(distance.Mul(i))
		if n.X >= 0 && n.X < width && n.Y >= 0 && n.Y < height {
			nodes = append(nodes, n)
		}
		i++
	}
	n = image.Point{0, 0}
	i = 0
	for n.X >= 0 && n.X < width && n.Y >= 0 && n.Y < height {
		n = a.Sub(distance.Mul(i))
		if n.X >= 0 && n.X < width && n.Y >= 0 && n.Y < height {
			nodes = append(nodes, n)
		}
		i++
	}
	return nodes
}

func part2(input string) int {
	antennas, width, height := makeAntennas(input)
	var listOfAllAntinodes []image.Point
	var nodesList [][]image.Point
	for _, listOnFrequency := range antennas {
		for i := 0; i < len(listOnFrequency); i++ {
			for j := i + 1; j < len(listOnFrequency); j++ {
				points := countAntinodesPart2(listOnFrequency[i], listOnFrequency[j], width, height)
				listOfAllAntinodes = unionPoints(listOfAllAntinodes, points)
				nodesList = append(nodesList, points)
			}
		}
	}
	drawGrid(antennas, nodesList, width, height)
	return len(listOfAllAntinodes)
}
