package handler

import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"math/rand"
	"net/http"
	"time"
)


type BankruptRequest struct {
	AccessKey int64  `json:"access_key"`
	Bankrupt int `json:"bankrupt"`
}

type Request struct {
	VacancyId int64 `json:"vacancy_id"`
}


func (h *Handler) issueBankrupt(c *gin.Context) {
	var input Request
	if err := c.BindJSON(&input); err != nil {
		newErrorResponse(c, http.StatusBadRequest, err.Error())
		return
	}
	fmt.Println("handler.issueBankrupt:", input)

	c.Status(http.StatusOK)

	go func() {
		time.Sleep(4 * time.Second)
		sendBankruptRequest(input)
	}()
}

func sendBankruptRequest(request Request) {

	var bankrupt = -1
	if rand.Intn(10) % 10 >= 2 {
	 bankrupt = rand.Intn(2)
	}

	answer := BankruptRequest{
		AccessKey: 123,
		Bankrupt: bankrupt,
	}

	client := &http.Client{}

	jsonAnswer, _ := json.Marshal(answer)
	bodyReader := bytes.NewReader(jsonAnswer)

	requestURL := fmt.Sprintf("http://127.0.0.1:8000/api/vacancies/%d/update_bankrupt/", request.VacancyId)

	req, _ := http.NewRequest(http.MethodPost, requestURL, bodyReader)

	req.Header.Set("Content-Type", "application/json")

	response, err := client.Do(req)
	if err != nil {
		fmt.Println("Error sending PUT request:", err)
		return
	}

	defer response.Body.Close()

	fmt.Println("PUT Request Status:", response.Status)
}
