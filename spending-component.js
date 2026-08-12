export default function(component) {

    const {
        data,
        parentElement,
        setTriggerValue
    } = component;

    const container =
        parentElement.querySelector("#spending-container");

    container.innerHTML = data.html;

    container.addEventListener("click", (event) => 
    {
        const button = event.target.closest(".budget-box");

        if (!button) {
            return;
        }

        //Clear previous selection
        container
            .querySelectorAll(".budget-box.selected")
            .forEach(box => box.classList.remove("selected"));
        
        //Animate selected box
        button.classList.add("selected");
        container.classList.add("has-selection");

        //Send to Python
        setTimeout(() => {
            setTriggerValue(
                "selected",
                {
                    category : button.dataset.category,
                    gao_code : button.dataset.gaocode
                }

            );
        }, 3000);
        
    });
}