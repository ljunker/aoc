package main

import (
	"aoc-go/2024-go/util"
	_ "embed"
	"fmt"
	"math"
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
	fmt.Println("Part 1:")
	part1Timed := util.MeasureRuntime(part1)
	ans := part1Timed(input)
	fmt.Println("Output:", ans)
	err := util.CopyToClipboard(fmt.Sprintf("%v", ans))
	if err != nil {
		_ = fmt.Errorf("error running copytoclipboard %w", err)
	}
	fmt.Println("Part 2:")
	part2Timed := util.MeasureRuntime(part2)
	ans = part2Timed(input)
	fmt.Println("Output:", ans)
	err = util.CopyToClipboard(fmt.Sprintf("%v", ans))
	if err != nil {
		_ = fmt.Errorf("error running copytoclipboard %w", err)
	}
}

func part1(input string) int {
	stones := getStones(input)
	length := blinkCache(stones, 25)
	return length
}

func printStones(stones []int) {
	for _, stone := range stones {
		fmt.Print(stone, " ")
	}
	fmt.Println()
}

func getStones(input string) []int {
	var stones []int
	for _, s := range strings.Split(strings.TrimSpace(input), " ") {
		num, _ := strconv.Atoi(s)
		stones = append(stones, num)
	}
	return stones
}

func powInt(x, y int) int {
	return int(math.Pow(float64(x), float64(y)))
}

func rules(stone int) []int {
	var newStones []int
	if stone == 0 {
		newStones = append(newStones, 1)
	} else {
		length := lenLoop(stone)
		if length%2 == 0 {
			leftStone := stone / powInt(10, length/2)
			rightStone := stone % powInt(10, length/2)
			newStones = append(newStones, leftStone)
			newStones = append(newStones, rightStone)
		} else {
			newStones = append(newStones, stone*2024)
		}
	}
	return newStones
}

func lenLoop(i int) int {
	if i == 0 {
		return 1
	}
	count := 0
	for i != 0 {
		i /= 10
		count++
	}
	return count
}

func blinkCache(stones []int, depth int) int {
	var dp func(int, int) int
	cache := map[[2]int]int{}

	dp = func(n, depth int) int {
		if value, ok := cache[[2]int{n, depth}]; ok {
			return value
		}

		newStones := rules(n)
		if depth == 1 {
			return len(newStones)
		}

		l := 0
		for _, m := range newStones {
			l += dp(m, depth-1)
		}

		cache[[2]int{n, depth}] = l
		return l
	}
	l := 0
	for _, stone := range stones {
		l += dp(stone, depth)
	}
	return l
}

func part2(input string) int {
	stones := getStones(input)
	length := blinkCache(stones, 75)
	return length
}
