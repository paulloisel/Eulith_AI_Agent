const API_KEY = "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"
const submitButton = document.querySelector('#submit')
const outPutElement = document.querySelector('#output')
const inputElement = document.querySelector('input')
const historyElement = document.querySelector('.history')
const buttonElement = document.querySelector('button')

function changeInput(value) {
    const inputElement = document.querySelector('input')
    inputElement.value = value
}

async function getMessage() {
    console.log('clicked')
    const options = {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${API_KEY}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model: 'davinci',
            prompt: inputElement.value,
            temperature: 0.2
        })
    }
    try {
        const response = await fetch('https://api.openai.com/v1/completions', options)
        const data = await response.json()
        console.log(data)
        outPutElement.textContent = data.choices[0].text
        if (data.choices[0].text && inputElement.value) {
            const pElement = document.createElement('p')
            pElement.textContent = inputElement.value
            pElement.addEventListener('click', () => changeInput(pElement.textContent))
            historyElement.append(pElement)
        }
    
    } catch (error){
        console.error(error)

    }
}

submitButton.addEventListener('click', getMessage)

function clearInput() {
    inputElement.value = ' '
}
buttonElement.addEventListener('click', clearInput)