package main

import (
	"aoc-go/util"
	_ "embed"
	"flag"
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
	var part int
	flag.IntVar(&part, "part", 2, "part 1 or 2")
	flag.Parse()
	fmt.Println("Running part", part)

	if part == 1 {
		ans := part1(input)
		fmt.Println("Output:", ans)
		err := util.CopyToClipboard(fmt.Sprintf("%v", ans))
		if err != nil {
			_ = fmt.Errorf("error running copytoclipboard %w", err)
		}
	} else {
		ans := part2(input)
		fmt.Println("Output:", ans)
		err := util.CopyToClipboard(fmt.Sprintf("%v", ans))
		if err != nil {
			_ = fmt.Errorf("error running copytoclipboard %w", err)
		}
	}
}

type Pair struct {
	left, right int
}

func getPairs(numbers []int) []Pair {
	var pairs []Pair
	for i := 0; i < len(numbers)-1; i++ {
		pairs = append(pairs, Pair{numbers[i], numbers[i+1]})
	}
	return pairs
}

func isAscending(pairs []Pair) bool {
	for _, pair := range pairs {
		if pair.left > pair.right {
			return false
		}
	}
	return true
}

func isDescending(pairs []Pair) bool {
	for _, pair := range pairs {
		if pair.left < pair.right {
			return false
		}
	}
	return true
}

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func differBy1To3(pairs []Pair) bool {
	for _, pair := range pairs {
		abs := Abs(pair.left - pair.right)
		if abs < 1 || abs > 3 {
			return false
		}
	}
	return true
}

func part1(input string) int {
	count := 0
	lines := strings.Split(input, "\n")
	for _, l := range lines {
		var numbers []int
		str := strings.Split(strings.TrimSpace(l), " ")
		for i := range str {
			num, _ := strconv.Atoi(str[i])
			numbers = append(numbers, num)
		}
		pairs := getPairs(numbers)
		if (isAscending(pairs) || isDescending(pairs)) && differBy1To3(pairs) {
			count++
		}
	}
	return count
}

func part2(input string) int {
	count := 0
	lines := strings.Split(input, "\n")
	for _, l := range lines {
		var numbers []int
		str := strings.Split(strings.TrimSpace(l), " ")
		for i := range str {
			num, _ := strconv.Atoi(str[i])
			numbers = append(numbers, num)
		}
		pairs := getPairs(numbers)
		if (isAscending(pairs) || isDescending(pairs)) && differBy1To3(pairs) {
			count++
		} else {
			for i := 0; i < len(numbers); i++ {
				var newNumbers []int
				for j := 0; j < len(numbers); j++ {
					if i != j {
						newNumbers = append(newNumbers, numbers[j])
					}
				}
				pairs = getPairs(newNumbers)
				if (isAscending(pairs) || isDescending(pairs)) && differBy1To3(pairs) {
					count++
					break
				}
			}
		}
	}
	return count
}
