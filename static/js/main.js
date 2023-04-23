<script>
    const suggestMoreButton = document.getElementById('suggest-more-button');
    const businessDescription = document.querySelector('textarea[name="business"]').value;

    suggestMoreButton.addEventListener('click', () => {
        const numDomains = 10;
        fetch('/suggest_more_domains', {
            method: 'POST',
            body: JSON.stringify({ business: businessDescription, num_domains: numDomains }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(results => {
            const resultsList = document.querySelector('.results');
            for (const [domain, available] of Object.entries(results)) {
                const listItem = document.createElement('li');
                listItem.innerHTML = `${domain} ${available ? '<span class="available">&#10004;</span>' : '<span class="not-available">&#10008;</span>'}`;
                resultsList.appendChild(listItem);
            }
        })
        .catch(error => console.error(error));
    });
</script>
