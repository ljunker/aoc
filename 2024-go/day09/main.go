package main

import (
	"aoc-go/2024-go/util"
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
	fmt.Println("Running Part 1")
	part1Timed := util.MeasureRuntime(part1)
	ans := part1Timed(input)
	fmt.Println("Output:", ans)
	err := util.CopyToClipboard(fmt.Sprintf("%v", ans))
	if err != nil {
		_ = fmt.Errorf("error running copytoclipboard %w", err)
	}
	fmt.Println("Running Part 2")
	part2Timed := util.MeasureRuntime(part2)
	ans = part2Timed(input)
	fmt.Println("Output:", ans)
	err = util.CopyToClipboard(fmt.Sprintf("%v", ans))
	if err != nil {
		_ = fmt.Errorf("error running copytoclipboard %w", err)
	}
}

func part1(input string) int {
	diskMap := getDiskmap(input)
	//writeRepresentation(diskMap)
	for !defragmented(diskMap) {
		spaceNumber := 0
		leftMostSpace := 0
		fileNumber := len(diskMap)
		rightMostFile := len(diskMap[fileNumber-1])
		found := false
		for i := 0; !found && i < len(diskMap); i++ {
			for j := 0; j < len(diskMap[i]); j++ {
				if diskMap[i][j] == -1 {
					spaceNumber = i
					leftMostSpace = j
					found = true
					break
				}
			}
		}
		found = false
		for i := len(diskMap) - 1; !found && i >= 0; i-- {
			for j := len(diskMap[i]) - 1; j >= 0; j-- {
				if diskMap[i][j] != -1 {
					fileNumber = i
					rightMostFile = j
					found = true
					break
				}
			}
		}
		if fileNumber < spaceNumber {
			break
		}
		diskMap[spaceNumber][leftMostSpace] = diskMap[fileNumber][rightMostFile]
		diskMap[fileNumber][rightMostFile] = -1
		//writeRepresentation(diskMap)
	}
	checkSum := checksum(diskMap)
	return checkSum
}

func checksum(diskMap [][]int) int {
	checkSum := 0
	i := 0
	for _, filesAndSpaces := range diskMap {
		for _, f := range filesAndSpaces {
			if f != -1 {
				checkSum += i * f
			}
			i++
		}
	}
	return checkSum
}

func getDiskmap(input string) [][]int {
	file := true
	fileID := 0
	counter := 0
	var diskMap [][]int
	for _, y := range strings.Split(input, "") {
		if file {
			diskMap = append(diskMap, []int{})
			number, _ := strconv.Atoi(y)
			for i := 0; i < number; i++ {
				diskMap[counter] = append(diskMap[counter], fileID)
			}
			fileID++
			counter++
			file = false
		} else {
			diskMap = append(diskMap, []int{})
			number, _ := strconv.Atoi(y)
			for i := 0; i < number; i++ {
				diskMap[counter] = append(diskMap[counter], -1)
			}
			counter++
			file = true
		}
	}
	return diskMap
}

func defragmented(diskMap [][]int) bool {
	number := true
	for _, filesAndSpaces := range diskMap {
		for _, f := range filesAndSpaces {
			if number && f == -1 {
				number = false
			}
			if !number && f != -1 {
				return false
			}
		}
	}
	return true
}

func writeRepresentation(diskMap [][]int) string {
	var sb strings.Builder
	for _, filesAndSpaces := range diskMap {
		for _, file := range filesAndSpaces {
			if file == -1 {
				sb.Write([]byte("."))
			} else {
				fileNumber := strconv.Itoa(file)
				sb.Write([]byte(fileNumber))
			}
		}
	}
	s := sb.String()
	//fmt.Println(s)
	return s
}

func part2(input string) int {
	diskMap := getDiskmap(input)
	i := len(diskMap) - 1
	if i%2 != 0 {
		i--
	}
	for ; i >= 0; i -= 2 {
		length := len(diskMap[i])
		//find a free space
		for j := 1; j < len(diskMap) && j < i; j += 2 {
			if len(diskMap[j]) < length {
				continue
			}
			firstFreeSpace := -1
			for k := 0; k < len(diskMap[j]); k++ {
				if diskMap[j][k] == -1 {
					firstFreeSpace = k
					break
				}
			}
			if firstFreeSpace == -1 {
				continue
			}
			if len(diskMap[j])-firstFreeSpace < length {
				continue
			}
			for k := 0; k < len(diskMap[i]); k++ {
				diskMap[j][k+firstFreeSpace] = diskMap[i][k]
				diskMap[i][k] = -1
			}
			break
		}
		//writeRepresentation(diskMap)
	}
	return checksum(diskMap)
}
