
if ! `id -u lld`; then
	useradd lld
fi

su lld -c /usr/libexec/tests/lld/run-lit-tests
