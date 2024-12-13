package util

import (
	"bytes"
	"fmt"
	"os/exec"
	"runtime"
	"strings"
)

func GetCurrentOS() string {
	return runtime.GOOS
}

func CopyToClipboard(text string) error {
	if GetCurrentOS() == "windows" {
		return CopyToClipboardWindows(text)
	} else {
		return CopyToClipboardMac(text)
	}
}

func CopyToClipboardMac(text string) error {
	command := exec.Command("pbcopy")
	command.Stdin = bytes.NewReader([]byte(text))

	if err := command.Start(); err != nil {
		return fmt.Errorf("error starting pbcopy command: %w", err)
	}

	err := command.Wait()
	if err != nil {
		return fmt.Errorf("error running pbcopy %w", err)
	}

	return nil
}

func CopyToClipboardWindows(text string) error {
	cmd := exec.Command("cmd", "/c", "clip")
	cmd.Stdin = strings.NewReader(text)

	if err := cmd.Start(); err != nil {
		return fmt.Errorf("error starting clipboard command: %w", err)
	}
	err := cmd.Wait()
	if err != nil {
		return fmt.Errorf("error running clipboard %w", err)
	}
	return nil
}
