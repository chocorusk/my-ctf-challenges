FROM sagemath/sagemath:10.7@sha256:4f5589eb6c565949a006f8665de2876b8414410daf5ac554f4434a15d4f3d528

USER sage
WORKDIR /app

COPY chal.sage .

CMD ["sage", "chal.sage"]