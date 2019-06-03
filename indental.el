;;; indental.el -- Major mode for Indental files

;; Author: mftrhu <mftrhu+indentalel@inventati.org>
;; Created: 2019-05-03
;; Keywords: Indental major-mode

;; Copyright 2019 mftrhu <mftrhu+indentalel@inventati.org>

;; Permission is hereby granted, free of charge, to any person obtaining
;; a copy of this software and associated documentation files (the
;; "Software"), to deal in the Software without restriction, including
;; without limitation the rights to use, copy, modify, merge, publish,
;; distribute, sublicense, and/or sell copies of the Software, and to
;; permit persons to whom the Software is furnished to do so, subject to
;; the following conditions:

;; The above copyright notice and this permission notice shall be
;; included in all copies or substantial portions of the Software.

;; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
;; EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
;; MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
;; NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
;; BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
;; ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
;; CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
;; SOFTWARE.

;;; Commentary:

;; This is a very, very simple major mode for the Indental data format,
;; providing basic syntax highlighting and hopefully, one day, other
;; niceties for editing Indental files.

;; This major mode was developed thanks to Scott Andrew Borton's Mode
;; Tutorial on EmacsWiki.

;; Indental: <https://wiki.xxiivv.com/indental>
;; Mode Tutorial: <https://www.emacswiki.org/emacs/ModeTutorial>

;;; Code:
(defvar indental-mode-hook nil)

(defvar indental-mode-map
  (make-sparse-keymap)
  "Keymap for the Indental major mode")

;;;###autoload
(add-to-list 'auto-mode-alist '("\\.ndtl\\'" . indental-mode))

;;; Font-lock regex/face definitions
(defconst indental-font-lock-keywords
  (list
   '("^;.*" . font-lock-comment-face)
   '("^[^ ].+$" . font-lock-constant-face)
   '("\\(\\(?:  \\)+\\)\\w+ : " . font-lock-builtin-face)
   ;; The following patterns mark-up constructs of my own little
   ;; markup language.
   '("\\*\\*\\(.*?\\)\\*\\*" . font-lock-warning-face)
   '("{b \\(.*?\\)}" . font-lock-warning-face)
   '("//\\(.*?\\)//" . font-lock-doc-face)
   '("{i \\(.*?\\)}" . font-lock-doc-face)
   ;; The following pattern requires `font-lock-multiline', and it
   ;; creates some slight issues during editing, colorizing the wrong
   ;; elements until the font-lock is refreshed.
   '("\\(\\(?:  \\)+\\)\\(\\w+\\)\\(\n\\1  \\)" . font-lock-builtin-face)
   )
  "Indental syntax highlighting")

;;; Mode definition
(define-derived-mode indental-mode fundamental-mode "Indental"
  ;; Set up font-lock
  (set (make-local-variable 'font-lock-multiline) t)
  (set (make-local-variable 'font-lock-defaults) '(indental-font-lock-keywords))
  (set (make-local-variable 'adaptive-fill-regexp)
       "[ 	]*\\(\\([-–!|#%;>*·•‣⁃◦&]+\\|[&#*|-]\\)[ 	]*\\)*")
  (visual-line-mode 1)
  (adaptive-wrap-prefix-mode 1)
  )

(provide 'indental-mode)

;;; indental.el ends here
;; Local Variables:
;; eval: (outshine-mode 1)
;; End:
