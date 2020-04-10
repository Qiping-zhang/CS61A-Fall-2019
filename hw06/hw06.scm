;;;;;;;;;;;;;;;
;; Questions ;;
;;;;;;;;;;;;;;;

; Scheme

(define (cddr s)
  (cdr (cdr s)))

(define (cadr s)
  (car (cdr s))
)

(define (caddr s)
  (car (cdr (cdr s)))
)

(define (sign x)
  (cond
      ((= x 0) 0)
        ((< x 0) -1)
        (else 1)
))

(define (square x) (* x x))

(define (pow b n)
  (cond
        ((= 0 n) 1)
          ((= 1 b) b)
            ((even? n) (square (pow b (/ n 2)))
                )
            ((odd? n) (* b (pow b (- n 1))))
            )
           )
      
  

(define (unique s)
   (if
           (null? s) 
             nil
           (cons (car s) (filter (lambda (x) (not (equal? x (car s)))) (unique (cdr s))
                                       )
                             )
                         )
           
                )
           
