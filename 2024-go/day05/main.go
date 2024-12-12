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

type rule struct {
	left, right int
}

func part1(input string) int {
	rules, updates := getRulesAndUpdates(input)
	sum := 0
	for _, update := range updates {
		valid := true
		for k, i := range update {
			for _, r := range rules {
				if r.left == k && update[r.right] != 0 {
					valid = valid && (i < update[r.right])
				}
			}
		}
		if valid {
			l := len(update) / 2
			for k, v := range update {
				if v-1 == l {
					sum += k
				}
			}
		}
	}
	return sum
}

func getRulesAndUpdates(input string) ([]rule, []map[int]int) {
	readRules := true
	var rules []rule
	var updates []map[int]int
	for _, s := range strings.Split(input, "\n") {
		if len(strings.TrimSpace(s)) == 0 {
			readRules = false
			continue
		}
		if readRules {
			leftRight := strings.Split(s, "|")
			left, _ := strconv.Atoi(leftRight[0])
			right, _ := strconv.Atoi(leftRight[1])
			rules = append(rules, rule{left: left, right: right})
		} else {
			numberStrings := strings.Split(s, ",")
			update := make(map[int]int)
			for i, n := range numberStrings {
				atoi, _ := strconv.Atoi(n)
				update[atoi] = i + 1
			}
			updates = append(updates, update)
		}
	}
	return rules, updates
}

func part2(input string) int {
	rules, updates := getRulesAndUpdates(input)
	sum := 0
	for _, update := range updates {
		valid := true
		for k, i := range update {
			for _, r := range rules {
				if r.left == k && update[r.right] != 0 {
					valid = valid && (i < update[r.right])
				}
			}
		}
		if !valid {
			sortedUpdate := sort(update, rules)
			l := len(sortedUpdate) / 2
			sum += sortedUpdate[l]
		}
	}
	return sum
}

func sort(update map[int]int, rules []rule) []int {
	var sortedUpdate []int
	for k, _ := range update {
		sortedUpdate = append(sortedUpdate, k)
	}
	// sort by rules, yes this is bubblesort shut up
	for n := len(sortedUpdate); n > 1; n-- {
		for i := 0; i < n-1; i = i + 1 {
			if checkRules(rules, sortedUpdate[i], sortedUpdate[i+1]) {
				sortedUpdate[i], sortedUpdate[i+1] = sortedUpdate[i+1], sortedUpdate[i]
			}
		}
	}
	return sortedUpdate
}

func checkRules(rules []rule, i int, i2 int) bool {
	for _, r := range rules {
		if r.left == i && r.right == i2 {
			return false
		}
		if r.left == i2 && r.right == i {
			return true
		}
	}
	return false
}
