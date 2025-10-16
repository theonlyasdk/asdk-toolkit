$(async function () {
    const tool_baseurl = "http://127.0.0.1:8080"; // for local testing
    // const tool_baseurl = "https://theonlyasdk.github.io/electronics-toolkit"; // use this for public url

    try {
        let response;
        response = await fetch('./data/tools_data.json');
        const data = await response.json();
        response = await fetch('./data/tools_icons.json');
        const icons = await response.json();

        let tools_section = $("#tools-section");
        tools_section.html("");

        Object.keys(data).forEach(key => {
            tools_section.append(`
                <div class="d-flex flex-row gap-2 justify-content-between">
                    <h4 class="m-0">${key}</h4>
                    <i class="bi ${icons[key]}" title="${key}"></i>
                </div>
                <hr class="mt-2" />
            `);

            let tool_card_container = `<div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3">`;
        
            data[key].forEach(tool => {
                const tool_source = `https://github.com/theonlyasdk/electronics-toolkit/${tool.url}`;
                const tool_url = `${tool_baseurl}/${tool.url}`;
        
                tool_card_container += `
                <div class="col d-flex">
                    <div class="card flex-fill">
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title mb-2">${tool.name}</h5>
                            <p class="card-text flex-grow-1">${tool.description}</p>
                            <div class="d-flex flex-row gap-2 w-100 align-items-end justify-content-end">
                                <a href="${tool_source}" class="btn btn-outline-primary mt-auto" target="_blank" title="View on GitHub">
                                    <i class="bi bi-github me-1"></i> GitHub
                                </a>
                                <a href="${tool_url}" class="btn btn-primary mt-auto" target="_blank">
                                    <i class="bi bi-box-arrow-up-right"></i> Open Tool
                                </a>
                            </div>
                        </div>
                    </div>
                </div>`;
            });

            tool_card_container += `</div>`;
            tools_section.append(tool_card_container);
        });

    } catch (err) {
        console.error("Failed to load tools: ", err);
        $("#tools-section").html(`
            <h5 class="text-danger">Failed to load tools data!</h5>
            <code>Reason: ${err}</code>
        `);
    }

    $(".theme-option").on("click", function (e) {
        e.preventDefault();
        const theme = $(this).data("theme");
        if (theme === "auto") {
            document.body.removeAttribute("data-bs-theme");
        } else {
            document.body.setAttribute("data-bs-theme", theme);
        }
    });
});