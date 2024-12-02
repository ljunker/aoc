package main

import (
	"aoc-go/util"
	_ "embed"
	"flag"
	"fmt"
	"regexp"
	"sort"
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

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func part1(input string) int {
	leftList, rightList := getLists(input)
	sort.Slice(leftList, func(i, j int) bool {
		return leftList[i] < leftList[j]
	})
	sort.Slice(rightList, func(i, j int) bool {
		return rightList[i] < rightList[j]
	})
	sumDistances := 0
	for i := 0; i < len(leftList); i++ {
		left := leftList[i]
		right := rightList[i]
		sumDistances += Abs(right - left)
	}
	return sumDistances
}

func getLists(input string) ([]int, []int) {
	lines := strings.Split(input, "\n")
	var leftList []int
	var rightList []int
	re := regexp.MustCompile(" +")
	for _, line := range lines {
		leftAndRight := re.Split(strings.Trim(line, "\r\n"), -1)
		number, _ := strconv.Atoi(leftAndRight[0])
		leftList = append(leftList, number)
		number, _ = strconv.Atoi(leftAndRight[1])
		rightList = append(rightList, number)
	}
	return leftList, rightList
}

func count[T any](slice []T, f func(T) bool) int {
	count := 0
	for _, s := range slice {
		if f(s) {
			count++
		}
	}
	return count
}

func part2(input string) int {
	leftList, rightList := getLists(input)
	sumSimilarities := 0
	for i := 0; i < len(leftList); i++ {
		left := leftList[i]
		occ := count(rightList, func(x int) bool {
			return x == left
		})
		sumSimilarities += occ * left
	}
	return sumSimilarities
}
