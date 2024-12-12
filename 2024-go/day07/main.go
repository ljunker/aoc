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
	sum := 0
	for _, s := range strings.Split(input, "\n") {
		split := strings.Split(s, ":")
		testValue, _ := strconv.Atoi(split[0])
		var values []int
		rightSides := strings.Split(strings.TrimSpace(split[1]), " ")
		for _, sp := range rightSides {
			value, _ := strconv.Atoi(sp)
			values = append(values, value)
		}
		var operators = make([]string, len(values)-1)
		possibleOperators := []string{"+", "*"}
		sum += calculate(testValue, values, possibleOperators, operators, 0, values[0])
	}
	return sum
}

func concat(i int, j int) int {
	var sb strings.Builder
	sb.WriteString(strconv.Itoa(i))
	sb.WriteString(strconv.Itoa(j))
	result, _ := strconv.Atoi(sb.String())
	return result
}

func calculate(testValue int, values []int, possibleOperators []string, operators []string, i int, current int) int {
	if i == len(operators) {
		return current
	}
	for _, op := range possibleOperators {
		operators[i] = op
		var result int
		switch operators[i] {
		case "+":
			result = current + values[i+1]
		case "*":
			result = current * values[i+1]
		case "||":
			result = concat(current, values[i+1])
		}
		res := calculate(testValue, values, possibleOperators, operators, i+1, result)
		if res == testValue {
			return res
		}
	}
	return 0
}

func part2(input string) int {
	sum := 0
	for _, s := range strings.Split(input, "\n") {
		split := strings.Split(s, ":")
		testValue, _ := strconv.Atoi(split[0])
		var values []int
		rightSides := strings.Split(strings.TrimSpace(split[1]), " ")
		for _, sp := range rightSides {
			value, _ := strconv.Atoi(sp)
			values = append(values, value)
		}
		var operators = make([]string, len(values)-1)
		possibleOperators := []string{"+", "*", "||"}
		sum += calculate(testValue, values, possibleOperators, operators, 0, values[0])
	}
	return sum
}
