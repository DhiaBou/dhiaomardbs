SELECT
    p."ParteiID",
    p."Beschreibung",
    COUNT(*)
FROM
    parteien p
JOIN
    kandidaten k ON p."ParteiID" = k."ParteiID"
JOIN
    stimmzettel stzl ON k."KandidatID" = stzl."Zweitstimme"
where k."StimmkreisId"=131
GROUP BY
        p."ParteiID",p."Beschreibung"
;





